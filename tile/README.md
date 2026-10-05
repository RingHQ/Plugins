# Tile

Arrange every window on the screen at once.

In a grid, in columns, or with the active window large and the others
stacked beside it.

## Actions

| Action | What it does |
|---|---|
| `tile.grid` | Every window gets a cell of a grid. |
| `tile.columns` | The windows stand side by side, all the same width. |
| `tile.master` | The active window takes the left 60%, the others share the rest. |

Only the windows of the current desktop on the monitor in use are moved.
The active window comes first; the others keep their order from left to
right. Your gaps are respected.

## Good to know

Undo brings back the active window only; the other windows stay where the
action put them.
