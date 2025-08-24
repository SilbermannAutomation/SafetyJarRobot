#!/usr/bin/env python3
"""
motor_controller.py
Hiwonder BUS-servo controller class (Raspberry Pi expansion board / black board).

- One shared Board connection (singleton) across all Motor instances.
- Per-motor control by BUS ID.
- Position in pulses (0..1000) or degrees (0..range_deg).
- Optional velocity (pulses/s or deg/s): class computes duration.
- Safe reads via thread + timeout (never blocks forever).

Requires:
    pip install pyserial  # if not already present
and Hiwonder's 'ros_robot_controller_sdk.py' available in PYTHONPATH.

Author: Yoav
"""

import time
from typing import Optional, Tuple
from controller.control_board_singleton import _BoardSingleton
from utils.util import Util

# ----------- Motor class -----------
class Motor:
    """
    Motor(servo_id, device='/dev/serial0', baud=1_000_000, name=None, range_deg=240.0, read_timeout=0.8)

    Methods:
      turnOnTorque() / turnOffTorque()
      readPosition(units='pulses'|'deg') -> int|float|None
      goToPosition(position, velocity=None, units='pulses'|'deg', hold=None, duration=None)
      stop()
      home(mid=500, duration=2.0)
      setSoftLimits(min_pulse, max_pulse)
      setAngleLimitToFirmware(min_pulse, max_pulse)  # writes to servo via controller
      readStatus() -> dict (vin_mV, temp_C, torque_on)
    """

    PULSE_MIN = 0
    PULSE_MAX = 1000
    MIN_DURATION_S = 0.15
    MAX_DURATION_S = 60.0
    SAFE_DEFAULT_DUR = 2.0

    def __init__(
        self,
        servo_id: int,
        device: str = "/dev/serial0",
        baud: int = 1_000_000,
        name: Optional[str] = None,
        range_deg: float = 240.0,
        read_timeout: float = 0.8,
    ):
        self.id = int(servo_id)
        self.name = name or f"servo_{self.id}"
        self.range_deg = float(range_deg)
        self.read_timeout = float(read_timeout)
        self.board = _BoardSingleton.get(device=device, baud=baud, timeout=5)

        # soft software clamps (optional)
        self.soft_min = self.PULSE_MIN
        self.soft_max = self.PULSE_MAX
        # self.turnOnTorque()

    # ---------- torque ----------
    def turnOnTorque(self):
        self.board.bus_servo_enable_torque(self.id, True)

    def turnOffTorque(self):
        self.board.bus_servo_enable_torque(self.id, False)

    # ---------- reads ----------
    def readPosition(self, units: str = "pulses"):
        """
        Read current position. Returns pulses (int) or degrees (float), or None if not available.
        """
        def _read():
            pos = self.board.bus_servo_read_position(self.id)
            # SDK may return scalar; normalize
            if isinstance(pos, (list, tuple)):
                pos = pos[-1]
            return int(pos)
        pulses = Util._threaded_read(_read, self.read_timeout)
        if pulses is None:
            return None
        if units.lower().startswith("deg"):
            return Util.deg_from_pulses(pulses, self.range_deg)
        return pulses

    def readStatus(self) -> dict:
        """Return basic telemetry (best-effort). Missing fields may be None."""
        def _vin():  return self.board.bus_servo_read_vin(self.id)
        def _tmp():  return self.board.bus_servo_read_temp(self.id)
        def _tq():   return self.board.bus_servo_read_torque_state(self.id)
        vin = Util._threaded_read(_vin, self.read_timeout)
        tmp = Util._threaded_read(_tmp, self.read_timeout)
        tq  = Util._threaded_read(_tq,  self.read_timeout)
        return {
            "id": self.id,
            "vin_mV": vin if isinstance(vin, int) else None,
            "temp_C": tmp if isinstance(tmp, int) else None,
            "torque_on": (tq == 1) if tq is not None else None
        }

    # ---------- motion ----------
    def _compute_duration(self, current_pulses: int, target_pulses: int,
                          velocity: Optional[float], units: str) -> Optional[float]:
        """
        Compute duration from a velocity (pulses/s or deg/s).
        """
        dist = abs(int(target_pulses) - int(current_pulses))
        if dist == 0:
            return self.MIN_DURATION_S
        if velocity is None or velocity <= 0:
            return None

        units = units.lower()
        if units.startswith("deg"):
            # velocity is deg/s -> convert to pulses/s
            pulses_per_deg = 1000.0 / self.range_deg
            vel_pulses = velocity * pulses_per_deg
        else:
            vel_pulses = velocity

        if vel_pulses <= 0:
            return None

        dur = dist / vel_pulses
        return Util._clamp(dur, self.MIN_DURATION_S, self.MAX_DURATION_S)

    def goToPosition(
        self,
        position,
        velocity: Optional[float] = None,
        units: str = "pulses",
        hold: Optional[bool] = None,
        duration: Optional[float] = None,
    ):
        """
        Move to target position.
          position: pulses (0..1000) or degrees (0..range_deg) depending on 'units'
          velocity: if provided, units:
                    - pulses/s when units='pulses'
                    - deg/s    when units='deg'
          hold: if False, torque is released after move (default True)
          duration: if given, overrides velocity-based timing

        Notes:
          - If readPosition() fails, falls back to SAFE_DEFAULT_DUR unless duration is given.
          - Soft-limits are applied to pulses target.
        """
        # Normalize target pulses
        if units.lower().startswith("deg"):
            target_pulses = Util.pulses_from_deg(float(position), self.range_deg)
        else:
            target_pulses = int(position)

        # Apply soft limits
        target_pulses = Util._clamp(target_pulses, self.soft_min, self.soft_max)

        # Ensure torque
        try:
            self.turnOnTorque()
            time.sleep(0.02)
        except Exception:
            pass

        # Read current pulses (for duration computation)
        curr = self.readPosition(units="pulses")
        if curr is None:
            curr = target_pulses  # so dist=0; will rely on duration/default

        # Determine duration
        if duration is not None:
            dur = Util._clamp(float(duration), self.MIN_DURATION_S, self.MAX_DURATION_S)
        else:
            dur = self._compute_duration(curr, target_pulses, velocity, units)
            if dur is None:
                dur = self.SAFE_DEFAULT_DUR

        # Send
        self.board.bus_servo_set_position(dur, [[self.id, int(target_pulses)]])

        # Wait slightly longer
        time.sleep(dur + 0.1)

        # Release torque unless told to hold
        if hold is False:
            try:
                self.turnOffTorque()
            except Exception:
                pass

    # CamelCase aliases to match your requested API names exactly
    def goToPositionDeg(self, degrees: float, velocity_deg: Optional[float] = None, hold: Optional[bool] = None, duration: Optional[float] = None):
        """Convenience: same as goToPosition(..., units='deg')."""
        return self.goToPosition(degrees, velocity=velocity_deg, units="deg", hold=hold, duration=duration)

    def turn_on_torque(self):  # snake_case alias
        return self.turnOnTorque()

    def turn_off_torque(self):
        return self.turnOffTorque()

    # ---------- other useful helpers ----------
    def stop(self):
        """Issue a stop command to this servo."""
        try:
            self.board.bus_servo_stop([self.id])
        except Exception:
            pass

    def home(self, mid: int = 500, duration: float = 2.0):
        """Move to mid position slowly."""
        mid = Util._clamp(int(mid), self.PULSE_MIN, self.PULSE_MAX)
        self.goToPosition(mid, velocity=None, units="pulses", hold=True, duration=duration)

    def nudge(self, delta_pulses: int = 10, duration: float = 0.6):
        """Small incremental move relative to current position."""
        curr = self.readPosition(units="pulses")
        if curr is None:
            curr = 500
        tgt = Util._clamp(curr + int(delta_pulses), self.soft_min, self.soft_max)
        self.goToPosition(tgt, duration=duration, units="pulses", hold=True)

    def setSoftLimits(self, min_pulse: int, max_pulse: int):
        """Set software clamps for safety."""
        min_pulse = Util._clamp(int(min_pulse), self.PULSE_MIN, self.PULSE_MAX)
        max_pulse = Util._clamp(int(max_pulse), self.PULSE_MIN, self.PULSE_MAX)
        if min_pulse > max_pulse:
            min_pulse, max_pulse = max_pulse, min_pulse
        self.soft_min, self.soft_max = min_pulse, max_pulse

    def setAngleLimitToFirmware(self, min_pulse: int, max_pulse: int):
        """
        Persist angle limits into the servo via the controller (bus_servo_set_angle_limit).
        Use with care; persists in servo memory.
        """
        min_pulse = Util._clamp(int(min_pulse), self.PULSE_MIN, self.PULSE_MAX)
        max_pulse = Util._clamp(int(max_pulse), self.PULSE_MIN, self.PULSE_MAX)
        if min_pulse > max_pulse:
            min_pulse, max_pulse = max_pulse, min_pulse
        self.board.bus_servo_set_angle_limit(self.id, [min_pulse, max_pulse])
        time.sleep(0.05)
