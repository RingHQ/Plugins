"""Swap: let the active window change places with another one."""


def _others(context):
    """Return the other windows on the monitor in use."""
    screen = context.monitor.geometry
    found = []
    for window in context.backend.get_windows():
        frame = window.geometry
        middle = (frame.x + frame.width // 2, frame.y + frame.height // 2)
        if window.id != context.window.id and screen.contains(*middle):
            found.append(window)
    return found


def _trade(context, other):
    """Send `other` to where the active window is; Ring does the other half."""
    target = other.geometry
    context.backend.set_geometry(other, context.window.geometry)
    return target


def largest(context):
    """Change places with the largest other window."""
    others = _others(context)
    if not others:
        return None
    return _trade(
        context, max(others, key=lambda window: window.geometry.width * window.geometry.height)
    )


def _position(window):
    return (window.geometry.x, window.geometry.y, window.id)


def _neighbour(context, step):
    others = _others(context)
    if not others:
        return None
    row = sorted([context.window, *others], key=_position)
    index = next(i for i, window in enumerate(row) if window.id == context.window.id)
    return _trade(context, row[(index + step) % len(row)])


def following(context):
    """Change places with the next window, going left to right."""
    return _neighbour(context, 1)


def previous(context):
    """Change places with the previous window, going left to right."""
    return _neighbour(context, -1)


def register(api):
    api.add_action("largest", largest, label="Swap with the largest window")
    api.add_action("next", following, label="Swap with the next window")
    api.add_action("previous", previous, label="Swap with the previous window")
