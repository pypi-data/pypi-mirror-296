# pitch/basketball.py
from .base import PitchBase
from ..geometry.line import Line
from ..geometry.arc import Arc
from ..geometry.circle import Circle


class BasketballCourt(PitchBase):
    """A class for plotting a customizable basketball court."""

    sport_type = "basketball"

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

        # Center circle
        self.elements.append(
            Circle(
                length / 2,
                width / 2,
                d["center_circle_radius"],
                color=lc,
                linewidth=lw,
                alpha=la,
                zorder=lz,
            )
        )

        # Half-court line
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

        # Three-point lines and arcs
        for side in [left, right]:
            # Baseline three-point lines
            self.elements.extend(
                [
                    Line(
                        side,
                        (width - d["three_point_radius"] * 2) / 2,
                        side + (1 if side == left else -1) * 0.0,
                        (width - d["three_point_radius"] * 2) / 2,
                        color=lc,
                        linewidth=lw,
                        alpha=la,
                        linestyle=ls,
                        zorder=lz,
                    ),
                    Line(
                        side,
                        (width + d["three_point_radius"] * 2) / 2,
                        side + (1 if side == left else -1) * 0.0,
                        (width + d["three_point_radius"] * 2) / 2,
                        color=lc,
                        linewidth=lw,
                        alpha=la,
                        linestyle=ls,
                        zorder=lz,
                    ),
                ]
            )

            # Three-point arc
            self.elements.append(
                Arc(
                    side + (1 if side == left else -1) * d["backboard_distance"],
                    width / 2,
                    d["three_point_radius"] * 2,
                    d["three_point_radius"] * 2,
                    angle=0,
                    theta1=-90 if side == left else 90,
                    theta2=90 if side == left else 270,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    zorder=lz,
                )
            )

        # Free throw circles
        for side in [
            left + d["free_throw_line_distance"],
            right - d["free_throw_line_distance"],
        ]:
            # Free throw semicircle (solid line)
            self.elements.append(
                Arc(
                    side,
                    width / 2,
                    d["free_throw_circle_radius"] * 2,
                    d["free_throw_circle_radius"] * 2,
                    angle=0,
                    theta1=-90,
                    theta2=90,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    zorder=lz,
                )
            )
            # Free throw semicircle (dashed line)
            self.elements.append(
                Arc(
                    side,
                    width / 2,
                    d["free_throw_circle_radius"] * 2,
                    d["free_throw_circle_radius"] * 2,
                    angle=0,
                    theta1=90,
                    theta2=270,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    linestyle="dashed",
                    zorder=lz,
                )
            )

        # Restricted areas
        for side in [left, right]:
            self.elements.append(
                Arc(
                    side + (1 if side == left else -1) * d["backboard_distance"],
                    width / 2,
                    d["restricted_area_radius"] * 2,
                    d["restricted_area_radius"] * 2,
                    angle=0,
                    theta1=0 if side == left else 180,
                    theta2=180 if side == left else 360,
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    zorder=lz,
                )
            )

        # Backboards
        for side in [left + d["backboard_distance"], right - d["backboard_distance"]]:
            self.elements.append(
                Line(
                    side,
                    (width / 2) - (d["backboard_width"] / 2),
                    side,
                    (width / 2) + (d["backboard_width"] / 2),
                    color=lc,
                    linewidth=lw,
                    alpha=la,
                    zorder=lz,
                )
            )

        # Additional elements can be added similarly (e.g., lanes, key areas)
