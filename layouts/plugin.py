"""Layouts: remember where your windows are and put them back later."""

import json
import os
from pathlib import Path

from ring.actions import Rect

SLOTS = 3


def _path():
    base = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / "ring" / "layouts.json"


def _load():
    try:
        data = json.loads(_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _store(data):
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=1), encoding="utf-8")
    temporary.replace(path)


def save(slot, context):
    """Remember the frame of every window on the current desktop."""
    entries = []
    for window in context.backend.get_windows():
        frame = window.geometry
        entries.append(
            {
                "app": window.app_id,
                "title": window.title,
                "frame": [frame.x, frame.y, frame.width, frame.height],
            }
        )
    data = _load()
    data[str(slot)] = entries
    _store(data)
    return None


def _match(entries, windows):
    """Pair saved frames with open windows: (window, frame) for each match.

    Window ids do not survive a restart, so windows are recognised by their
    application, preferring the one whose title is the same as well.
    """
    free = list(windows)
    pairs = []
    for same_title in (True, False):
        for entry in entries:
            if entry.get("used"):
                continue
            for window in free:
                titles_agree = window.title == entry.get("title")
                if window.app_id == entry.get("app") and (titles_agree or not same_title):
                    entry["used"] = True
                    free.remove(window)
                    pairs.append((window, Rect(*entry["frame"])))
                    break
    return pairs


def restore(slot, context):
    """Put the windows back where the layout has them."""
    entries = _load().get(str(slot))
    if not isinstance(entries, list):
        return None
    try:
        pairs = _match([dict(entry) for entry in entries], context.backend.get_windows())
    except (TypeError, ValueError, KeyError, AttributeError):
        return None
    target = None
    for window, frame in pairs:
        if window.id == context.window.id:
            # Ring moves the active window itself, so it can be undone.
            target = frame
        elif window.geometry != frame:
            context.backend.set_geometry(window, frame)
    return target


def register(api):
    for slot in range(1, SLOTS + 1):
        api.add_action(
            f"save_{slot}",
            lambda context, slot=slot: save(slot, context),
            label=f"Save layout {slot}",
        )
        api.add_action(
            f"restore_{slot}",
            lambda context, slot=slot: restore(slot, context),
            label=f"Restore layout {slot}",
        )
