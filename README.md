# Ring plugins

Plugins for [Ring](https://github.com/RingHQ/Ring), the radial window
snapper for Linux. A plugin adds actions that go on a key or a direction of
the ring like any built-in one, or reacts to what Ring does.

| Plugin | What it does |
|---|---|
| [layouts](layouts/) | Remember where your windows are and put them back later. |
| [presets](presets/) | The window centered, at one of three sizes. |
| [rgb](rgb/) | The ring runs through the rainbow while it is open. |
| [swap](swap/) | Let the active window change places with another one. |
| [tile](tile/) | Arrange every window on the screen at once. |

## Installing a plugin

```sh
ring plugins available        # what is in this repository
ring plugins install tile     # copy it to ~/.config/ring/plugins/
ring plugins enable tile      # load it
```

Then put its actions, for example `tile.grid`, on a key or a direction in
the settings window. `ring plugins update tile` fetches the current version,
`ring plugins remove tile` deletes it.

Plugins run inside Ring with your full permissions. Read what you enable.

## How this repository is laid out

One folder per plugin, named like the plugin: lowercase letters, digits and
`_`. That name is the first half of its actions' names (`tile.grid`).

```
tile/
├── README.md    the plugin's name (first heading) and description (first paragraph)
└── plugin.py    the plugin: a register(api) function
```

A plugin may bring more Python files in its folder and import them with
`from . import ...`. How to write one is described in Ring's
[docs/PLUGINS.md](https://github.com/RingHQ/Ring/blob/main/docs/PLUGINS.md).

## License

GPL-3.0-only, like Ring.
