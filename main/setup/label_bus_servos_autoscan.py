#!/usr/bin/env python3
"""
Hiwonder BUS-servo labeling wizard (auto-scan + confirm).
- Scans IDs in a configurable range (default 1..30)
- For each ID, gently wiggles and asks for confirmation (y/n)
- If confirmed, prompts for a friendly name and stores mapping
- Saves mapping to JSON and CSV at the end

Usage:
  python3 label_bus_servos_autoscan.py

You can tweak the CONFIG section below (ID range, wiggle amplitude, timings, etc.).
"""

import csv
import json
import sys
import time
import signal

from controller import ros_robot_controller_sdk as rrc

# ------------------- CONFIG -------------------
DEVICE = "/dev/serial0"
BAUD   = 1_000_000

SCAN_ID_START = 1              # inclusive
SCAN_ID_END   = 30             # inclusive

MID = 500                      # center pulse (0..1000)
WIGGLE_LOW, WIGGLE_HIGH = 470, 530     # gentle ±30 around center
WIGGLE_DURATION = 1.8          # seconds each leg
SETTLE = 0.10                  # add-on settle delay after a leg
PAUSE_BETWEEN_IDS = 0.4        # pause between IDs

OUTPUT_JSON = "controller/servo_map.json"
# ---------------------------------------------

RUN = True
def _stop(sig, frame):
    global RUN
    RUN = False
    print("\nStopping ...")
signal.signal(signal.SIGINT, _stop)

def wiggle_one(board : rrc.Board, sid : int, low=WIGGLE_LOW, high=WIGGLE_HIGH, duration=WIGGLE_DURATION):
    """
    Very gentle, slow wiggle for a single bus-servo ID (write-only, no reads).
    Sequence: torque on -> go mid -> high -> low -> high.
    """
    # Ensure torque
    try:
        board.bus_servo_enable_torque(sid, 1)
        time.sleep(0.02)
    except Exception:
        # Ignore if the ID doesn't exist; we’re probing
        pass

    # Move to mid
    try:
        board.bus_servo_set_position(duration, [[sid, MID]])
        time.sleep(duration + SETTLE)
    except Exception:
        return

    # Wiggle sequence
    try:
        board.bus_servo_set_position(duration, [[sid, high]])
        time.sleep(duration + SETTLE)
        board.bus_servo_set_position(duration, [[sid, low]])
        time.sleep(duration + SETTLE)
        board.bus_servo_set_position(duration, [[sid, high]])
        time.sleep(duration + SETTLE)
    except Exception:
        return

def ask_yes_no(prompt):
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"): return True
        if ans in ("n", "no"):  return False
        if ans in ("q", "quit"): return None
        print("  Please answer y / n (or q to quit).")

def main():
    print("Connecting to Hiwonder controller ...")
    board = rrc.Board(device=DEVICE, baudrate=BAUD, timeout=5)
    board.enable_reception(True)

    # Small cue we started
    board.set_led(0.05, 0.05, repeat=2)
    board.set_buzzer(2400, 0.03, 0.05, 2)

    print("\n=== BUS-servo auto-scan & labeling ===")
    print(f"Scanning IDs {SCAN_ID_START}..{SCAN_ID_END}")
    print("For each ID I will wiggle slowly; confirm if you SAW that joint move.")
    print("Type y/n, or q to finish early.\n")

    mapping = {}   # name -> id
    used_ids = set()

    # Optional: global torque enable (harmless if unsupported)
    try:
        board.bus_servo_enable_torque(254, 1)
        time.sleep(0.05)
    except Exception:
        pass

    try:
        for sid in range(SCAN_ID_START, SCAN_ID_END + 1):
            if not RUN:
                break

            print(f"\n--- Probing ID {sid} ---")
            wiggle_one(board, sid)

            # Ask user for confirmation
            yn = ask_yes_no("Did a joint move for this ID? [y/n/q]: ")
            if yn is None:  # quit
                break
            if yn is False:
                print("  Not confirmed; continuing scan.")
                time.sleep(PAUSE_BETWEEN_IDS)
                continue

            # Confirmed: name it
            while True:
                name = input("  Enter a unique name for this joint (e.g., base, shoulder): ").strip()
                if name == "":
                    print("  Name cannot be empty.")
                    continue
                if name in mapping:
                    print("  That name is already used; choose another.")
                    continue
                if sid in used_ids:
                    print("  This ID is already recorded; choose a different ID or name.")
                    continue
                mapping[name] = sid
                used_ids.add(sid)
                print(f"  Recorded mapping: {name} -> {sid}")
                break

            time.sleep(PAUSE_BETWEEN_IDS)

    except KeyboardInterrupt:
        print("\nInterrupted.")

    # Best-effort stop on recorded servos
    try:
        if used_ids:
            board.bus_servo_stop(list(used_ids))
    except Exception:
        pass

    # Show results
    print("\n=== Final mapping (name -> ID) ===")
    if not mapping:
        print("No mappings recorded.")
    else:
        for k, v in mapping.items():
            print(f"{k}: {v}")

        # Save JSON
        try:
            with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
                json.dump(mapping, f, ensure_ascii=False, indent=2)
            print(f"\nSaved JSON: {OUTPUT_JSON}")
        except Exception as e:
            print(f"\nCould not save {OUTPUT_JSON}: {e}")

    print("\nDone.")

if __name__ == "__main__":
    main()
