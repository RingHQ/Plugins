"""Daily: how many windows Ring moved each day, and a note at round numbers."""

import json
import os
import shutil
import subprocess
from datetime import date, timedelta
from pathlib import Path

MILESTONES = (100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000)
KEPT_DAYS = 400


def _path():
    base = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / "ring" / "daily.json"


def _load():
    try:
        data = json.loads(_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(day): int(count) for day, count in data.items() if isinstance(count, int)}


def _store(days):
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    kept = dict(sorted(days.items())[-KEPT_DAYS:])
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(kept), encoding="utf-8")
    temporary.replace(path)


def _notify(title, text):
    program = shutil.which("notify-send")
    if program is not None:
        subprocess.Popen(
            [program, "--app-name=Ring", "--icon=ring", title, text],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def _total():
    """Return Ring's own counter, which also counts the time before this plugin."""
    from ring.stats import Stats, default_stats_path

    return Stats(default_stats_path()).total


def summary(days, today):
    """Return the lines of the last seven days, today first."""
    lines = []
    for back in range(7):
        day = today - timedelta(days=back)
        name = "Today" if back == 0 else day.strftime("%a %d %b")
        lines.append(f"{name}: {days.get(day.isoformat(), 0)}")
    return lines


def applied(action, window, rect):
    days = _load()
    today = date.today().isoformat()
    days[today] = days.get(today, 0) + 1
    _store(days)
    total = _total()
    if total in MILESTONES:
        _notify(f"{total:,} windows moved", "Ring has been busy.")


def show(context):
    """Show the last seven days in a notification."""
    _notify("Windows moved", "\n".join(summary(_load(), date.today())))
    return None


def register(api):
    api.on("action_applied", applied)
    api.add_action("show", show, label="Show the last seven days")
