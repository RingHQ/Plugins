# Daily

Counts the windows Ring moved each day, with a note at round numbers.

The note is a desktop notification when the used counter reaches 100, 250,
500, 1,000 and so on.

## Actions

| Action | What it does |
|---|---|
| `daily.show` | Show the counts of the last seven days in a notification. |

The counting starts on the day the plugin is enabled. The milestones follow
Ring's own counter, so they include everything from before.

## Good to know

- The counts are kept in `~/.local/state/ring/daily.json`, for the last 400
  days.
- Notifications are sent with `notify-send` (package `libnotify`); without
  it the plugin only counts.
- `daily.show` itself counts as a use of Ring.
