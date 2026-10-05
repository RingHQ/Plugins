# Presets

The window centered on the screen, at one of three sizes.

## Actions

| Action | What it does |
|---|---|
| `presets.small` | Centered, half the width and height of the screen. |
| `presets.medium` | Centered, 65% of the width and height. |
| `presets.large` | Centered, 80% of the width and height. |

The sizes are shares of the monitor in use without its panels.

## Good to know

The three make a good cycle on one key: pressing it again steps to the next
size.

```toml
[keybindings]
KEY_C = ["presets.small", "presets.medium", "presets.large"]
```
