"""Tile: arrange every window on the screen at once."""

import math

from ring.actions import Rect


def _windows(context):
    """Return the windows on the monitor in use, the active one first."""
    screen = context.monitor.geometry
    others = []
    for window in context.backend.get_windows():
        frame = window.geometry
        middle = (frame.x + frame.width // 2, frame.y + frame.height // 2)
        if window.id != context.window.id and screen.contains(*middle):
            others.append(window)
    # Left to right, then top to bottom, so the result follows what was there.
    others.sort(key=lambda window: (window.geometry.x, window.geometry.y))
    return [context.window, *others]


def _split(start, length, count, gap):
    """Cut a stretch into `count` pieces with `gap` between them."""
    usable = length - gap * (count - 1)
    edges = [start + round(usable * index / count) + gap * index for index in range(count)]
    sizes = [
        round(usable * (index + 1) / count) - round(usable * index / count)
        for index in range(count)
    ]
    return list(zip(edges, sizes, strict=True))


def _area(context):
    gaps = getattr(context, "gaps", None)
    outer = gaps.outer if gaps else 0
    inner = gaps.inner if gaps else 0
    return context.area.inset(outer), inner


def _apply(context, windows, frames):
    """Move every window but the active one; Ring moves that one itself."""
    for window, frame in zip(windows[1:], frames[1:], strict=True):
        context.backend.set_geometry(window, frame)
    return frames[0]


def grid(context):
    """Give every window a cell of a grid; the last row shares what is left."""
    windows = _windows(context)
    area, gap = _area(context)
    columns = math.ceil(math.sqrt(len(windows)))
    rows = math.ceil(len(windows) / columns)
    frames = []
    for row, (y, height) in enumerate(_split(area.y, area.height, rows, gap)):
        in_row = windows[row * columns : (row + 1) * columns]
        for x, width in _split(area.x, area.width, len(in_row), gap):
            frames.append(Rect(x, y, width, height))
    return _apply(context, windows, frames)


def columns(context):
    """Put the windows side by side, all the same width."""
    windows = _windows(context)
    area, gap = _area(context)
    frames = [
        Rect(x, area.y, width, area.height)
        for x, width in _split(area.x, area.width, len(windows), gap)
    ]
    return _apply(context, windows, frames)


def master(context):
    """The active window takes the left 60%, the others stack on the right."""
    windows = _windows(context)
    area, gap = _area(context)
    if len(windows) == 1:
        return area
    main = round((area.width - gap) * 0.6)
    side_x, side_width = area.x + main + gap, area.width - main - gap
    frames = [Rect(area.x, area.y, main, area.height)]
    for y, height in _split(area.y, area.height, len(windows) - 1, gap):
        frames.append(Rect(side_x, y, side_width, height))
    return _apply(context, windows, frames)


def register(api):
    api.add_action("grid", grid, label="Tile all windows in a grid")
    api.add_action("columns", columns, label="Tile all windows in columns")
    api.add_action("master", master, label="This window large, the others stacked")
