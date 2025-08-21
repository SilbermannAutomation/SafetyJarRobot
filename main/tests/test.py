#!/usr/bin/env python3
"""
Hiwonder bus-servo slow test (no reads, no blocking).
- Enables torque on likely IDs
- Centers them slowly
- Then gently sweeps a few millimeters back/forth very slowly
"""

import time
import signal
from controller import ros_robot_controller_sdk as rrc

# <<< Adjust this list if your IDs differ >>>
LIKELY_IDS = [1, 2, 3, 4, 5, 6]   # Hiwonder bus-servo IDs

RUN = True

def _stop(sig, frame):
    global RUN
    RUN = False
    print("\nStopping ...")

signal.signal(signal.SIGINT, _stop)

def send_positions(board, ids, pulse, duration_s):
    """Send one slow multi-servo position command."""
    if not ids:
        return
    positions = [[sid, int(pulse)] for sid in ids]
    board.bus_servo_set_position(duration_s, positions)

def main():
    # GPIO UART on the Hiwonder HAT; 1,000,000 baud is the SDK default
    board = rrc.Board(device="/dev/serial0", baudrate=1_000_000, timeout=5)
    board.enable_reception(True)

    # Small visual cue that we started
    board.set_led(0.05, 0.05, repeat=2)
    board.set_buzzer(2400, 0.03, 0.05, 2)

    # Try broadcast torque enable (many LX servos accept 254); also try per-ID
    try:
        board.bus_servo_enable_torque(254, 1)  # harmless if not supported
        time.sleep(0.05)
    except Exception:
        pass
    for sid in LIKELY_IDS:
        try:
            board.bus_servo_enable_torque(sid, 1)
            time.sleep(0.02)
        except Exception:
            # Ignore missing IDs; we are sending blind
            pass

    print("Centering all likely IDs to 500 over 4 s ...")
    send_positions(board, LIKELY_IDS, 500, duration_s=4.0)
    time.sleep(4.2)

    print("Gently sweeping (480→520) very slowly. Ctrl+C to stop.")
    pulses = [430, 570]
    idx = 0
    while RUN:
        send_positions(board, LIKELY_IDS, pulses[idx], duration_s=3.5)
        idx ^= 1
        # Wait slightly longer than duration to avoid overlap
        for _ in range(36):
            if not RUN: break
            time.sleep(0.1)

    # Try to stop motion gracefully
    try:
        board.bus_servo_stop(LIKELY_IDS)
    except Exception:
        pass
    print("Done.")

if __name__ == "__main__":
    main()
