# pitch/tennis.py
from .base import PitchBase
from ..geometry.line import Line


class TennisCourt(PitchBase):
    """A class for plotting a customizable tennis court."""

    sport_type = "tennis"

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
        singles_width = d["singles_width"]
        service_line_distance = d["service_line_distance"]
        left = 0
        right = length
        bottom = 0
        top = width

        # Update dimensions for axis limits
        self.dimensions.update(
            {"left": bottom, "right": top, "bottom": left, "top": right}
        )

        # Rotate the court to be horizontal
        # Outer boundaries (doubles court)
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
                ),  # Left boundary
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
                ),  # Top boundary
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
                ),  # Right boundary
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
                ),  # Bottom boundary
            ]
        )

        # Singles sidelines
        offset = (width - singles_width) / 2
        self.elements.extend(
            [
                Line(
                    bottom + offset,
                    left,
                    bottom + offset,
                    right,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
                Line(
                    top - offset,
                    left,
                    top - offset,
                    right,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
            ]
        )

        # Net line
        self.elements.append(
            Line(
                bottom,
                length / 2,
                top,
                length / 2,
                color=lc,
                linewidth=lw,
                alpha=la,
                linestyle=ls,
                zorder=lz,
            )
        )

        # Service lines
        self.elements.extend(
            [
                Line(
                    bottom + offset,
                    left + service_line_distance,
                    top - offset,
                    left + service_line_distance,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
                Line(
                    bottom + offset,
                    right - service_line_distance,
                    top - offset,
                    right - service_line_distance,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
            ]
        )

        # Center service lines
        self.elements.append(
            Line(
                width / 2,
                left + service_line_distance,
                width / 2,
                right - service_line_distance,
                color=lc,
                linewidth=lw,
                alpha=la,
                linestyle=ls,
                zorder=lz,
            )
        )
