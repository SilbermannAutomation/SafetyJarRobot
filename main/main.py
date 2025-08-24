from drivers.servo import Motor

# ----------- Example usage -----------
if __name__ == "__main__":
    # Simple demo: set up one motor and try a few moves.
    # Adjust SERVO_ID below.
    SERVO_ID = 2

    m = Motor(SERVO_ID, device="/dev/serial0", baud=1_000_000, name="base", range_deg=240.0)
    print("Status:", m.readStatus())

    # Gentle center
    print("Homing...")
    m.home(mid=500, duration=2.0)

    # Move by pulses at 120 pulses/s
    print("Move to 650 pulses @ 120 pulses/s ...")
    m.goToPosition(650, velocity=120, units="pulses", hold=True)

    # Move by degrees at 45 deg/s (range 240° assumed)
    print("Move to 30° @ 45 deg/s ...")
    m.goToPosition(30.0, velocity=45.0, units="deg", hold=True)

    # Nudge + stop + torque off
    print("Nudge + stop + torque off ...")
    m.nudge(+20)
    m.stop()
    m.turnOffTorque()
    print("Done.")