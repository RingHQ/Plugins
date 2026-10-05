# Layouts

Remember where your windows are and put them back later.

There are three layouts to save into.

## Actions

| Action | What it does |
|---|---|
| `layouts.save_1`, `save_2`, `save_3` | Remember the frame of every window on the current desktop. |
| `layouts.restore_1`, `restore_2`, `restore_3` | Move the windows back to where that layout has them. |

A layout survives restarts. Windows are recognised by their application, and
by their title where several windows of one application are open; a window
that was not there when the layout was saved is left alone.

## Good to know

- Layouts are kept in `~/.local/state/ring/layouts.json`, which holds the
  titles of the windows that were open.
- Minimized windows and windows on other desktops are neither saved nor
  moved.
- Undo brings back the active window only.
