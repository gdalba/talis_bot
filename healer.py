import argparse
import io
import time
from contextlib import redirect_stderr, redirect_stdout

import psutil
import win32api
import win32con
import win32gui
import win32process
from mouse import left as mouse_left

from pointers import Pointers

cords_team =({
            "yourself": [45, 45],
            "member_1": [25, 205],
            "member_2": [25, 285],
            "member_3": [25, 365],
            "member_4": [25, 445],
            })

def run_quietly(func, *args, **kwargs):
    sink = io.StringIO()
    with redirect_stdout(sink), redirect_stderr(sink):
        return func(*args, **kwargs)


def parse_watch_pids(raw):
    if not raw:
        return []

    pids = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            pids.append(int(token))
        except ValueError:
            continue
    return sorted(set(pids))


def parse_slots(raw):
    if not raw:
        return []

    slots = []
    for token in raw.split(","):
        token = token.strip().lower()
        if not token:
            continue
        if token in cords_team:
            slots.append(token)
    return slots


def discover_client_pids():
    pids = []
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        try:
            if (proc.info.get("name") or "").lower() == "client.exe":
                pids.append(proc.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return sorted(set(pids))


class Healer:
    def __init__(
        self,
        info_pid,
        heal_key_1="6",
        heal_key_2="5",
        mana_key="9",
        watch_pids=None,
        low_hp_threshold=3500,
        critical_hp_threshold=2000,
        poll_interval=0.25,
        mana_interval=8.0,
        maintenance_interval=10.0,
        critical_burst=2,
    ):
        self.info_pid = info_pid

        if heal_key_1.lower() != "none":
            self.heal_key_1 = heal_key_1
        else:
            self.heal_key_1 = None

        self.heal_key_2 = heal_key_2
        self.mana_key = mana_key
        self.watch_pids = sorted(set(watch_pids or []))

        self.low_hp_threshold = low_hp_threshold
        self.critical_hp_threshold = critical_hp_threshold
        self.poll_interval = poll_interval
        self.mana_interval = mana_interval
        self.maintenance_interval = maintenance_interval
        self.critical_burst = max(1, int(critical_burst))

        self.info_hwnd = None
        self._pointer_cache = {}
        self._self_pointer = None
        self._last_mana_at = 0.0
        self._last_maintenance_at = 0.0
        self._last_action = ""
        self._selected_slot = None
        self._pid_to_slot = {}
        self._slot_to_pid = {}

    def send_key(self, hwnd, key):
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, ord(key.upper()), 0)
        win32api.SendMessage(hwnd, win32con.WM_KEYUP, ord(key.upper()), 0)

    def find_game_window_title_by_pid(self, pid):
        window_title = None

        def enum_windows_callback(window_hwnd, _):
            nonlocal window_title
            try:
                _, window_pid = win32process.GetWindowThreadProcessId(window_hwnd)
                if window_pid == pid:
                    window_title = win32gui.GetWindowText(window_hwnd)
                    return False
            except Exception:
                pass
            return True

        win32gui.EnumWindows(enum_windows_callback, None)
        return window_title

    def find_game_window_by_title(self, title):
        return win32gui.FindWindow(None, title)

    def setup_window(self):
        info_title = self.find_game_window_title_by_pid(self.info_pid)
        if info_title:
            self.info_hwnd = self.find_game_window_by_title(info_title)

    def _normalize_name(self, value):
        if not isinstance(value, str):
            return ""
        return value.strip().lower()

    def _send_click(self, x, y):
        mouse_left(self.info_hwnd, int(x), int(y))

    def _click_slot(self, slot_name, force=False):
        if not force and slot_name == self._selected_slot:
            return False

        coords = cords_team.get(slot_name)
        if not coords:
            return False

        self._send_click(coords[0], coords[1])
        self._selected_slot = slot_name
        return True

    def _select_slot(self, slot_name):
        did_click = self._click_slot(slot_name, force=False)
        if not did_click:
            return

        coords = cords_team.get(slot_name)
        self._log_action(f"Healer: selected {slot_name} at {coords}.")

    def run_debug_click_test(self, slots, cycles=3, delay=0.6):
        self.setup_window()
        if not self.info_hwnd:
            print("Exiting: No valid game window found.")
            return

        valid_slots = [slot for slot in slots if slot in cords_team]
        if not valid_slots:
            print("Debug click: no valid slots selected.")
            return

        cycles = max(1, int(cycles))
        delay = max(0.05, float(delay))

        print(
            "Debug click mode started "
            f"(pid={self.info_pid}, slots={valid_slots}, cycles={cycles}, delay={delay}s)."
        )

        for cycle in range(1, cycles + 1):
            for slot_name in valid_slots:
                coords = cords_team[slot_name]
                print(f"Debug click: cycle {cycle}/{cycles}, slot={slot_name}, coords={coords}")
                self._click_slot(slot_name, force=True)
                time.sleep(delay)

        print("Debug click mode completed.")

    def _refresh_self_pointer(self):
        if self._self_pointer is not None:
            return
        try:
            self._self_pointer = run_quietly(Pointers, self.info_pid)
        except Exception:
            self._self_pointer = None

    def _log_action(self, message):
        if message != self._last_action:
            print(message)
            self._last_action = message

    def _resolve_watch_pids(self):
        if self.watch_pids:
            return [pid for pid in self.watch_pids if pid != self.info_pid]

        return [pid for pid in discover_client_pids() if pid != self.info_pid]

    def _sync_pointer_cache(self, watched_pids):
        watched = set(watched_pids)

        for pid in list(self._pointer_cache.keys()):
            if pid not in watched:
                self._pointer_cache.pop(pid, None)

        for pid in watched_pids:
            if pid in self._pointer_cache:
                continue
            try:
                self._pointer_cache[pid] = run_quietly(Pointers, pid)
            except Exception:
                continue

    def _refresh_team_slot_mapping(self, watched_pids):
        self._refresh_self_pointer()
        if self._self_pointer is None:
            return

        slot_name_by_team_name = {}
        team_getters = {
            "member_1": self._self_pointer.team_name_1,
            "member_2": self._self_pointer.team_name_2,
            "member_3": self._self_pointer.team_name_3,
            "member_4": self._self_pointer.team_name_4,
        }

        for slot_name, getter in team_getters.items():
            try:
                team_member_name = self._normalize_name(run_quietly(getter))
            except Exception:
                team_member_name = ""

            if team_member_name and team_member_name != "offline account":
                slot_name_by_team_name[team_member_name] = slot_name

        updated_pid_to_slot = {}
        updated_slot_to_pid = {}

        for pid in watched_pids:
            ptr = self._pointer_cache.get(pid)
            if ptr is None:
                continue

            try:
                char_name = self._normalize_name(run_quietly(ptr.get_char_name))
            except Exception:
                char_name = ""

            slot_name = slot_name_by_team_name.get(char_name)
            if slot_name and slot_name not in updated_slot_to_pid:
                updated_pid_to_slot[pid] = slot_name
                updated_slot_to_pid[slot_name] = pid

        # Keep prior mapping when names are temporarily unreadable.
        for pid in watched_pids:
            if pid in updated_pid_to_slot:
                continue
            prev_slot = self._pid_to_slot.get(pid)
            if prev_slot and prev_slot not in updated_slot_to_pid:
                updated_pid_to_slot[pid] = prev_slot
                updated_slot_to_pid[prev_slot] = pid

        self._pid_to_slot = updated_pid_to_slot
        self._slot_to_pid = updated_slot_to_pid

    def _collect_team_hp(self, watched_pids):
        hp_by_pid = {}
        for pid in watched_pids:
            ptr = self._pointer_cache.get(pid)
            if ptr is None:
                continue

            try:
                hp = run_quietly(ptr.get_hp)
            except Exception:
                hp = None

            if isinstance(hp, (int, float)):
                hp_by_pid[pid] = int(hp)

        return hp_by_pid

    def _send_burst(self, key, count, delay_seconds=0.16):
        for _ in range(count):
            self.send_key(self.info_hwnd, key)
            time.sleep(delay_seconds)

    def _choose_target_pid(self, hp_by_pid):
        if not hp_by_pid:
            return None, None

        member_1_pid = self._slot_to_pid.get("member_1")
        if member_1_pid is not None:
            member_1_hp = hp_by_pid.get(member_1_pid)
            if member_1_hp is not None and member_1_hp <= self.low_hp_threshold:
                return member_1_pid, member_1_hp

        target_pid = min(hp_by_pid, key=hp_by_pid.get)
        return target_pid, hp_by_pid[target_pid]

    def _run_maintenance(self, now):
        if self.heal_key_1 and (now - self._last_maintenance_at) >= self.maintenance_interval:
            self.send_key(self.info_hwnd, self.heal_key_1)
            self._last_maintenance_at = now

        if self.mana_key and (now - self._last_mana_at) >= self.mana_interval:
            self.send_key(self.info_hwnd, self.mana_key)
            self._last_mana_at = now

    def _close_pointer_cache(self):
        self._pointer_cache.clear()
        self._self_pointer = None

    def _smart_heal_loop(self):
        refresh_interval = 2.0
        next_refresh_at = 0.0
        watched_pids = []

        while True:
            now = time.time()

            if now >= next_refresh_at:
                watched_pids = self._resolve_watch_pids()
                self._sync_pointer_cache(watched_pids)
                self._refresh_team_slot_mapping(watched_pids)
                next_refresh_at = now + refresh_interval

            hp_by_pid = self._collect_team_hp(watched_pids)
            target_pid, target_hp = self._choose_target_pid(hp_by_pid)
            target_slot = self._pid_to_slot.get(target_pid)

            if target_hp is None:
                self._log_action("Healer: no readable target HP; maintenance mode.")
                self._run_maintenance(now)
            elif target_hp <= self.critical_hp_threshold:
                if target_slot:
                    self._select_slot(target_slot)
                self._log_action(
                    f"Healer: CRITICAL target PID {target_pid} slot={target_slot} HP={target_hp}; burst heal x{self.critical_burst}."
                )
                self._send_burst(self.heal_key_2, self.critical_burst)
                self._run_maintenance(now)
            elif target_hp <= self.low_hp_threshold:
                if target_slot:
                    self._select_slot(target_slot)
                self._log_action(
                    f"Healer: low target PID {target_pid} slot={target_slot} HP={target_hp}; single heal."
                )
                self.send_key(self.info_hwnd, self.heal_key_2)
                time.sleep(0.16)
                self._run_maintenance(now)
            else:
                self._log_action(f"Healer: stable; lowest PID {target_pid} slot={target_slot} HP={target_hp}.")
                self._run_maintenance(now)

            time.sleep(self.poll_interval)

    def start_healer(self):
        self.setup_window()
        if not self.info_hwnd:
            print("Exiting: No valid game window found.")
            return

        print(
            "Healer smart mode started "
            f"(pid={self.info_pid}, low_hp={self.low_hp_threshold}, critical_hp={self.critical_hp_threshold})."
        )

        try:
            self._smart_heal_loop()
        finally:
            self._close_pointer_cache()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart healer that reacts to teammate HP pointers.")
    parser.add_argument("info_pid", type=int, help="Healer client PID.")
    parser.add_argument("heal_key_1", type=str, help="Maintenance key or 'none'.")
    parser.add_argument("heal_key_2", type=str, help="Main heal key.")
    parser.add_argument("mana_key", type=str, help="Mana key.")
    parser.add_argument(
        "--watch-pids",
        type=str,
        default="",
        help="Comma-separated client PIDs to monitor. If omitted, monitors all other open client.exe PIDs.",
    )
    parser.add_argument("--low-hp", type=int, default=3500, help="Heal when HP is <= this value.")
    parser.add_argument("--critical-hp", type=int, default=2000, help="Burst-heal when HP is <= this value.")
    parser.add_argument("--poll-interval", type=float, default=0.25, help="Polling interval in seconds.")
    parser.add_argument("--mana-interval", type=float, default=8.0, help="Mana key interval in seconds.")
    parser.add_argument(
        "--maintenance-interval",
        type=float,
        default=10.0,
        help="Maintenance key interval in seconds.",
    )
    parser.add_argument("--critical-burst", type=int, default=2, help="Burst heal key presses on critical HP.")
    parser.add_argument(
        "--debug-click",
        action="store_true",
        help="Run click test mode only (no healing logic).",
    )
    parser.add_argument(
        "--debug-slots",
        type=str,
        default="member_1",
        help="Comma-separated slot names to click in debug mode (e.g. member_1,member_2,yourself).",
    )
    parser.add_argument("--debug-cycles", type=int, default=3, help="Number of click cycles in debug mode.")
    parser.add_argument("--debug-delay", type=float, default=0.6, help="Delay between debug clicks in seconds.")
    args = parser.parse_args()

    healer = Healer(
        info_pid=args.info_pid,
        heal_key_1=args.heal_key_1,
        heal_key_2=args.heal_key_2,
        mana_key=args.mana_key,
        watch_pids=parse_watch_pids(args.watch_pids),
        low_hp_threshold=args.low_hp,
        critical_hp_threshold=args.critical_hp,
        poll_interval=args.poll_interval,
        mana_interval=args.mana_interval,
        maintenance_interval=args.maintenance_interval,
        critical_burst=args.critical_burst,
    )
    if args.debug_click:
        healer.run_debug_click_test(
            slots=parse_slots(args.debug_slots),
            cycles=args.debug_cycles,
            delay=args.debug_delay,
        )
    else:
        healer.start_healer()
