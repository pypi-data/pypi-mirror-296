# pitch/handball.py
from .base import PitchBase
from ..geometry.line import Line
from ..geometry.arc import Arc


class HandballCourt(PitchBase):
    """A class for plotting a customizable handball court."""

    sport_type = "handball"

    def __init__(self, **kwargs):
        super().__init__(pitch_type="standard", **kwargs)
        self._create_court()

    def _create_court(self):
        d = self.dimensions
        lw = self.linewidth
        lc = self.line_color or "black"
        la = self.line_alpha
        ls = self.linestyle
        lz = self.line_zorder

        length = d["length"]
        width = d["width"]
        goal_area_radius = d["goal_area_radius"]
        dotted_line_distance = d["dotted_line_distance"]
        left = 0
        right = length
        bottom = 0
        top = width

        # Update dimensions for axis limits
        self.dimensions.update(
            {"left": left, "right": right, "bottom": bottom, "top": top}
        )

        # Outer boundaries
        self.elements.extend(
            [
                Line(
                    left,
                    bottom,
                    right,
                    bottom,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
                Line(
                    right,
                    bottom,
                    right,
                    top,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
                Line(
                    right,
                    top,
                    left,
                    top,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle=ls,
                    zorder=lz,
                ),
                Line(
                    left,
                    top,
                    left,
                    bottom,
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
                length / 2,
                bottom,
                length / 2,
                top,
                color=lc,
                linewidth=lw,
                alpha=la,
                linestyle=ls,
                zorder=lz,
            )
        )

        # Goal areas
        for x in [left, right]:
            direction = 1 if x == left else -1
            # Solid line arcs for goal area
            self.elements.append(
                Arc(
                    x + direction * goal_area_radius,
                    width / 2,
                    goal_area_radius * 2,
                    goal_area_radius * 2,
                    angle=0,
                    theta1=270 if x == left else 90,
                    theta2=90 if x == left else 270,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    zorder=lz,
                )
            )
            # Dotted line arcs for free throw line
            self.elements.append(
                Arc(
                    x + direction * dotted_line_distance,
                    width / 2,
                    dotted_line_distance * 2,
                    dotted_line_distance * 2,
                    angle=0,
                    theta1=270 if x == left else 90,
                    theta2=90 if x == left else 270,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle="dashed",
                    zorder=lz,
                )
            )
