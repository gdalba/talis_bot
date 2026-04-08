import argparse
import time

import psutil
import win32api
import win32con
import win32gui
import win32process
from mouse import left as mouse_left

from pointers import Pointers


# Party panel click coordinates (matches current setup used in healer.py).
SLOT_COORDS = {
    "member_1": [25, 205],
    "member_2": [25, 285],
    "member_3": [25, 365],
    "member_4": [25, 445],
}

SLOT_ORDER = ["member_1", "member_2", "member_3", "member_4"]


def parse_pid_list(raw):
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


def discover_client_pids():
    pids = []
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        try:
            if (proc.info.get("name") or "").lower() == "client.exe":
                pids.append(proc.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return sorted(set(pids))


def send_key(hwnd, key):
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, ord(key.upper()), 0)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, ord(key.upper()), 0)


def find_window_title_by_pid(pid):
    window_title = None

    def enum_windows_callback(hwnd, _):
        nonlocal window_title
        try:
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == pid:
                title = win32gui.GetWindowText(hwnd)
                if title:
                    window_title = title
                    return False
        except Exception:
            pass
        return True

    win32gui.EnumWindows(enum_windows_callback, None)
    return window_title


def find_window_handle_by_pid(pid):
    title = find_window_title_by_pid(pid)
    if not title:
        return None
    return win32gui.FindWindow(None, title)


def build_watch_list(info_pid, watch_pids):
    if watch_pids:
        return [pid for pid in watch_pids if pid != info_pid]
    return [pid for pid in discover_client_pids() if pid != info_pid]


def assign_slots(watch_pids):
    pid_to_slot = {}
    for index, pid in enumerate(watch_pids):
        if index >= len(SLOT_ORDER):
            break
        pid_to_slot[pid] = SLOT_ORDER[index]
    return pid_to_slot


def refresh_pointers(pointer_by_pid, watch_pids):
    watched = set(watch_pids)

    for pid in list(pointer_by_pid.keys()):
        if pid not in watched:
            pointer_by_pid.pop(pid, None)

    for pid in watch_pids:
        if pid in pointer_by_pid:
            continue
        try:
            pointer_by_pid[pid] = Pointers(pid)
        except Exception:
            continue


def collect_hp(pointer_by_pid, watch_pids):
    hp_by_pid = {}
    for pid in watch_pids:
        pointer = pointer_by_pid.get(pid)
        if pointer is None:
            continue

        try:
            hp = pointer.get_hp()
        except Exception:
            hp = None

        if isinstance(hp, (int, float)):
            hp_by_pid[pid] = int(hp)

    return hp_by_pid


def update_max_hp(max_hp_by_pid, hp_by_pid):
    for pid, hp in hp_by_pid.items():
        previous_max = max_hp_by_pid.get(pid, 0)
        if hp > previous_max:
            max_hp_by_pid[pid] = hp


def build_hp_percent(hp_by_pid, max_hp_by_pid):
    percent_by_pid = {}
    for pid, hp in hp_by_pid.items():
        max_hp = max_hp_by_pid.get(pid)
        if isinstance(max_hp, (int, float)) and max_hp > 0:
            percent_by_pid[pid] = (float(hp) / float(max_hp)) * 100.0
    return percent_by_pid


def choose_lowest_percent_target(percent_by_pid):
    if not percent_by_pid:
        return None, None

    target_pid = min(percent_by_pid, key=percent_by_pid.get)
    return target_pid, percent_by_pid[target_pid]


def maybe_click_slot(hwnd, slot_name, selected_slot):
    if not slot_name or slot_name == selected_slot:
        return selected_slot

    coords = SLOT_COORDS.get(slot_name)
    if not coords:
        return selected_slot

    mouse_left(hwnd, int(coords[0]), int(coords[1]))
    return slot_name


def run_maintenance(hwnd, heal_key_1, mana_key, now, timers, maintenance_interval, mana_interval):
    if heal_key_1 and heal_key_1.lower() != "none":
        if now - timers["last_maintenance"] >= maintenance_interval:
            send_key(hwnd, heal_key_1)
            timers["last_maintenance"] = now

    if mana_key and mana_key.lower() != "none":
        if now - timers["last_mana"] >= mana_interval:
            send_key(hwnd, mana_key)
            timers["last_mana"] = now


def print_once(message, state):
    if message != state["last_message"]:
        print(message)
        state["last_message"] = message


def smart_heal_loop(
    info_pid,
    hwnd,
    heal_key_1,
    heal_key_2,
    mana_key,
    watch_pids,
    heal_below_pct,
    poll_interval,
    refresh_seconds,
    mana_interval,
    maintenance_interval,
):
    pointer_by_pid = {}
    max_hp_by_pid = {}
    pid_to_slot = {}

    state = {
        "last_message": "",
        "selected_slot": None,
        "next_refresh_at": 0.0,
    }

    timers = {
        "last_mana": 0.0,
        "last_maintenance": 0.0,
    }

    watched_pids = []

    while True:
        now = time.time()

        if now >= state["next_refresh_at"]:
            watched_pids = build_watch_list(info_pid, watch_pids)
            refresh_pointers(pointer_by_pid, watched_pids)
            pid_to_slot = assign_slots(watched_pids)
            state["next_refresh_at"] = now + refresh_seconds

            print_once(f"Watching pids: {watched_pids}", state)

        hp_by_pid = collect_hp(pointer_by_pid, watched_pids)
        update_max_hp(max_hp_by_pid, hp_by_pid)
        percent_by_pid = build_hp_percent(hp_by_pid, max_hp_by_pid)

        target_pid, target_percent = choose_lowest_percent_target(percent_by_pid)
        target_hp = hp_by_pid.get(target_pid)
        target_slot = pid_to_slot.get(target_pid)

        if target_percent is None:
            print_once("No readable HP percent. Maintenance only.", state)
            run_maintenance(
                hwnd,
                heal_key_1,
                mana_key,
                now,
                timers,
                maintenance_interval,
                mana_interval,
            )

        elif target_percent <= float(heal_below_pct):
            state["selected_slot"] = maybe_click_slot(hwnd, target_slot, state["selected_slot"])
            print_once(
                f"HEAL: pid={target_pid} slot={target_slot} hp={target_hp} pct={target_percent:.1f}%",
                state,
            )
            send_key(hwnd, heal_key_2)
            time.sleep(0.16)

            run_maintenance(
                hwnd,
                heal_key_1,
                mana_key,
                now,
                timers,
                maintenance_interval,
                mana_interval,
            )

        else:
            print_once(
                f"STABLE: pid={target_pid} slot={target_slot} hp={target_hp} pct={target_percent:.1f}%",
                state,
            )
            run_maintenance(
                hwnd,
                heal_key_1,
                mana_key,
                now,
                timers,
                maintenance_interval,
                mana_interval,
            )

        time.sleep(max(0.05, float(poll_interval)))


def main():
    parser = argparse.ArgumentParser(description="Super simple healer loop for learning and quick edits.")
    parser.add_argument("info_pid", type=int, help="PID of healer client.")
    parser.add_argument("heal_key_1", type=str, help="Maintenance key (or none).")
    parser.add_argument("heal_key_2", type=str, help="Main heal key.")
    parser.add_argument("mana_key", type=str, help="Mana key (or none).")

    parser.add_argument("--watch-pids", type=str, default="", help="Comma-separated teammate PIDs.")
    parser.add_argument("--heal-below-pct", type=float, default=70.0, help="Heal when HP percent is at or below this value.")
    parser.add_argument("--poll-interval", type=float, default=0.25, help="Main loop sleep in seconds.")
    parser.add_argument("--refresh-seconds", type=float, default=2.0, help="How often to refresh watch list.")
    parser.add_argument("--mana-interval", type=float, default=8.0, help="Mana key interval in seconds.")
    parser.add_argument(
        "--maintenance-interval",
        type=float,
        default=10.0,
        help="Maintenance key interval in seconds.",
    )

    args = parser.parse_args()

    hwnd = find_window_handle_by_pid(args.info_pid)
    if not hwnd:
        print("No game window found for healer PID.")
        return

    watch_pids = parse_pid_list(args.watch_pids)
    print("Simple healer started.")
    print(f"Healer pid: {args.info_pid}")
    print(f"Watch pids (initial): {watch_pids if watch_pids else 'auto-discover'}")
    print(f"Heal below: {args.heal_below_pct:.1f}%")

    smart_heal_loop(
        info_pid=args.info_pid,
        hwnd=hwnd,
        heal_key_1=args.heal_key_1,
        heal_key_2=args.heal_key_2,
        mana_key=args.mana_key,
        watch_pids=watch_pids,
        heal_below_pct=args.heal_below_pct,
        poll_interval=args.poll_interval,
        refresh_seconds=args.refresh_seconds,
        mana_interval=args.mana_interval,
        maintenance_interval=args.maintenance_interval,
    )


if __name__ == "__main__":
    main()
