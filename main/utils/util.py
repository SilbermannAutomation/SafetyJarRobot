import threading
import queue

class Util:
    @staticmethod
    def _lerp(i, j, k):
        return float((1 - k) * i + j * k)

    @staticmethod
    def _invlerp(i, j, k):
        return float((k - i) / (j - i))

    @staticmethod
    def _x_round(x):
        return float(round(x*4) / 4)

    @staticmethod
    def _angle_to_position(degrees):
        if not isinstance(degrees, float) or degrees < -125.0 or degrees > 125.0:
            raise ValueError('Parameter \'degrees\' must be a float value between -125.0 and 125.0')
        x = Util._x_round(degrees)
        y = Util._invlerp(-125.0, 125.0, x)
        return int(Util._lerp(0, 1000, y))

    @staticmethod
    def _position_to_angle(position):
        if not isinstance(position, int) or position < 0 or position > 1000:
            raise ValueError('Parameter \'position\' must be and int value between 0 and 1000')

        return Util._lerp(-125.0, 125.0, position / 1000)
    
    @staticmethod
    def _clamp(x, lo, hi):
        return lo if x < lo else hi if x > hi else x

    @staticmethod
    def pulses_from_deg(deg: float, range_deg: float) -> int:
        """Map degrees (0..range_deg) -> pulses (0..1000)."""
        deg = Util._clamp(deg, 0.0, range_deg)
        return int(round(1000.0 * (deg / range_deg)))

    @staticmethod
    def deg_from_pulses(pulses: int, range_deg: float) -> float:
        """Map pulses (0..1000) -> degrees (0..range_deg)."""
        pulses = Util._clamp(int(pulses), 0, 1000)
        return (pulses / 1000.0) * range_deg

    @staticmethod
    def _threaded_read(fn, timeout_s: float):
        """Run a blocking SDK read in a thread; return None on timeout/failure."""
        q = queue.Queue(maxsize=1)
        def _w():
            try:
                val = fn()
                q.put(val)
            except Exception as e:
                q.put(e)
        t = threading.Thread(target=_w, daemon=True)
        t.start()
        t.join(timeout_s)
        if t.is_alive():
            return None
        res = q.get()
        if isinstance(res, Exception):
            return None
        return res