"""RGB: the ring runs through the rainbow while it is open."""

import colorsys
import time

# Seconds for one trip round the color wheel, and milliseconds per step.
CYCLE_SECONDS = 3.0
FRAME_MS = 33


def color(hue, saturation=0.85, value=1.0):
    """Return the color at `hue` (0 to 1, wrapping) as "#rrggbb"."""
    red, green, blue = colorsys.hsv_to_rgb(hue % 1.0, saturation, value)
    return f"#{round(red * 255):02x}{round(green * 255):02x}{round(blue * 255):02x}"


def colors(seconds):
    """Return accent, gradient and ring color for a point in time."""
    hue = seconds / CYCLE_SECONDS
    # The lit segment fades into a neighbouring color; the rest of the ring
    # glows more dimly, half a wheel behind, so the segment stands out.
    return color(hue), color(hue + 0.2), color(hue + 0.5, 0.9, 0.6)


class Rainbow:
    def __init__(self, api):
        self._api = api
        self._timer = None

    def start(self, window):
        if self._timer is None:
            # Only here: the service has a Qt event loop, `ring snap` has not.
            from PySide6.QtCore import QTimer

            self._timer = QTimer()
            self._timer.setInterval(FRAME_MS)
            self._timer.timeout.connect(self.step)
        self.step()
        self._timer.start()

    def stop(self, applied):
        # Nothing runs while the ring is closed.
        if self._timer is not None:
            self._timer.stop()

    def step(self):
        accent, gradient, ring = colors(time.monotonic())
        self._api.set_colors(accent=accent, gradient=gradient, ring=ring)


def register(api):
    if getattr(api, "version", 1) < 2:
        raise RuntimeError("this plugin needs a newer Ring (one with api.set_colors)")
    rainbow = Rainbow(api)
    api.on("menu_opened", rainbow.start)
    api.on("menu_closed", rainbow.stop)
