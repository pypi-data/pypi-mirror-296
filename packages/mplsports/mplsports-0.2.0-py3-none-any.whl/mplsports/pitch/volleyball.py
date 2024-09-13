# pitch/volleyball.py
from .base import PitchBase
from ..geometry.line import Line


class VolleyballCourt(PitchBase):
    """A class for plotting a customizable volleyball court."""

    sport_type = "volleyball"

    def __init__(self, **kwargs):
        super().__init__(pitch_type="standard", **kwargs)
        self._create_court()

    def _create_court(self):
        d = self.dimensions
        lw = self.linewidth
        lc = self.line_color or "white"
        la = self.line_alpha
        ls = self.linestyle
        lz = self.line_zorder

        length = d["length"]
        width = d["width"]
        attack_line_distance = d["attack_line_distance"]
        left = 0
        right = length
        bottom = 0
        top = width

        # Update dimensions for axis limits
        self.dimensions.update(
            {"left": bottom, "right": top, "bottom": left, "top": right}
        )

        # Rotate the court to be horizontal
        # Outer boundaries
        self.elements.extend(
            [
                Line(
                    bottom,
                    left,
                    bottom,
                    right,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
                Line(
                    bottom,
                    right,
                    top,
                    right,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
                Line(
                    top,
                    right,
                    top,
                    left,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
                Line(
                    top,
                    left,
                    bottom,
                    left,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
            ]
        )

        # Center line
        self.elements.append(
            Line(
                bottom,
                length / 2,
                top,
                length / 2,
                color=lc,
                linewidth=d["center_line_width"],
                alpha=la,
                linestyle=ls,
                zorder=lz,
            )
        )

        # Attack lines
        self.elements.extend(
            [
                Line(
                    bottom,
                    (length / 2) - attack_line_distance,
                    top,
                    (length / 2) - attack_line_distance,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
                Line(
                    bottom,
                    (length / 2) + attack_line_distance,
                    top,
                    (length / 2) + attack_line_distance,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
            ]
        )
