"""Presets: the window centered, at one of three sizes."""

from ring.actions import Rect

# Share of the work area's width and height each size takes.
SIZES = {"small": 0.5, "medium": 0.65, "large": 0.8}


def _centered(context, share):
    area = context.area
    width, height = round(area.width * share), round(area.height * share)
    return Rect(
        area.x + (area.width - width) // 2,
        area.y + (area.height - height) // 2,
        width,
        height,
    )


def register(api):
    for name, share in SIZES.items():
        api.add_action(
            name,
            lambda context, share=share: _centered(context, share),
            label=f"Centered, {name}",
        )
