import argparse
import io
import json
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone

import psutil
import win32gui
import win32process

from pointers import Pointers


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def emit(payload):
    print(json.dumps(payload, ensure_ascii=True), flush=True)


def discover_client_pids():
    pids = []
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        try:
            name = (proc.info.get("name") or "").lower()
            if name == "client.exe":
                pids.append(proc.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return sorted(set(pids))


def get_window_title_for_pid(pid):
    result = {"title": "N/A"}

    def callback(hwnd, _):
        try:
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == pid:
                title = win32gui.GetWindowText(hwnd)
                if title:
                    result["title"] = title
                    return False
        except Exception:
            return True
        return True

    try:
        win32gui.EnumWindows(callback, None)
    except Exception:
        pass
    return result["title"]


def safe_call(getter):
    try:
        return run_quietly(getter), None
    except Exception as exc:
        return None, str(exc)


def run_quietly(func, *args, **kwargs):
    # Suppress noisy prints from pointer resolution internals.
    sink = io.StringIO()
    with redirect_stdout(sink), redirect_stderr(sink):
        return func(*args, **kwargs)


def close_pointer(ptr):
    # Best effort cleanup for pymem process handle.
    try:
        if hasattr(ptr, "pm") and hasattr(ptr.pm, "close_process"):
            ptr.pm.close_process()
    except Exception:
        pass


def build_snapshot(pid, ptr):
    name, name_err = safe_call(ptr.get_char_name)
    level, level_err = safe_call(ptr.get_level)
    hp, hp_err = safe_call(ptr.get_hp)
    x, x_err = safe_call(ptr.get_x)
    y, y_err = safe_call(ptr.get_y)

    window_title = get_window_title_for_pid(pid)

    snapshot = {
        "type": "snapshot",
        "timestamp": utc_now_iso(),
        "pid": pid,
        "window_title": window_title,
        "name": name,
        "level": level,
        "hp": hp,
        "x": x,
        "y": y,
        "hp_pointer": getattr(ptr, "HP_POINTER", None),
        "errors": {
            "name": name_err,
            "level": level_err,
            "hp": hp_err,
            "x": x_err,
            "y": y_err,
        },
    }
    return snapshot


def run(interval_seconds):
    pointers_by_pid = {}

    emit(
        {
            "type": "status",
            "timestamp": utc_now_iso(),
            "status": "started",
            "message": "client pointer tracker started",
            "interval_seconds": interval_seconds,
        }
    )

    try:
        while True:
            live_pids = discover_client_pids()

            for pid in list(pointers_by_pid.keys()):
                if pid not in live_pids:
                    close_pointer(pointers_by_pid.pop(pid))
                    emit(
                        {
                            "type": "status",
                            "timestamp": utc_now_iso(),
                            "status": "pid_removed",
                            "pid": pid,
                            "message": "client process closed",
                        }
                    )

            for pid in live_pids:
                ptr = pointers_by_pid.get(pid)
                if ptr is None:
                    try:
                        ptr = run_quietly(Pointers, pid)
                        pointers_by_pid[pid] = ptr
                        emit(
                            {
                                "type": "status",
                                "timestamp": utc_now_iso(),
                                "status": "pid_added",
                                "pid": pid,
                                "message": "tracking started for pid",
                            }
                        )
                    except Exception as exc:
                        emit(
                            {
                                "type": "status",
                                "timestamp": utc_now_iso(),
                                "status": "pid_open_failed",
                                "pid": pid,
                                "error": str(exc),
                            }
                        )
                        continue

                snapshot = build_snapshot(pid, ptr)

                if snapshot["hp"] is None:
                    emit(
                        {
                            "type": "status",
                            "timestamp": utc_now_iso(),
                            "status": "hp_unavailable",
                            "pid": pid,
                            "hp_pointer": snapshot.get("hp_pointer"),
                            "detail": snapshot["errors"],
                            "message": "HP is unavailable for this PID; tracker is still running.",
                        }
                    )

                emit(snapshot)

            if not live_pids:
                emit(
                    {
                        "type": "status",
                        "timestamp": utc_now_iso(),
                        "status": "idle",
                        "message": "no client.exe processes found",
                    }
                )

            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        emit(
            {
                "type": "status",
                "timestamp": utc_now_iso(),
                "status": "stopped",
                "message": "tracker interrupted",
            }
        )
        return 0
    finally:
        for ptr in pointers_by_pid.values():
            close_pointer(ptr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Track core memory pointers for all open client.exe processes.")
    parser.add_argument("--interval", type=float, default=0.5, help="Polling interval in seconds (default: 0.5).")
    args = parser.parse_args()

    if args.interval <= 0:
        emit(
            {
                "type": "fatal",
                "timestamp": utc_now_iso(),
                "error": "invalid_interval",
                "message": "--interval must be greater than zero",
            }
        )
        sys.exit(2)

    sys.exit(run(args.interval))
