# pitch/soccer.py
from .base import PitchBase
from ..geometry.line import Line
from ..geometry.arc import Arc
from ..geometry.circle import Circle


class SoccerPitch(PitchBase):
    """A class for plotting a customizable soccer pitch."""

    sport_type = "soccer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_pitch()

    def _apply_customizations(self):
        """Apply customizations specific to soccer pitch elements."""
        # This method can be expanded to adjust element styles based on parameters
        pass

    def _create_pitch(self):
        d = self.dimensions
        lw = d["line_width"]
        length = d["length"]
        width = d["width"]
        penalty_area_length = d["penalty_area_length"]
        penalty_area_width = d["penalty_area_width"]
        goal_area_length = d["goal_area_length"]
        goal_area_width = d["goal_area_width"]
        center_circle_radius = d["center_circle_radius"]

        # Outer boundaries
        self.elements.extend(
            [
                Line(0, 0, length, 0, linewidth=lw),  # Bottom boundary
                Line(length, 0, length, width, linewidth=lw),  # Right boundary
                Line(length, width, 0, width, linewidth=lw),  # Top boundary
                Line(0, width, 0, 0, linewidth=lw),  # Left boundary
            ]
        )

        # Halfway line
        self.elements.append(Line(length / 2, 0, length / 2, width, linewidth=lw))

        # Center circle
        self.elements.append(
            Circle(length / 2, width / 2, center_circle_radius, linewidth=lw)
        )

        # Penalty areas
        self.elements.extend(
            [
                # Left penalty area
                Line(
                    0,
                    (width - penalty_area_width) / 2,
                    penalty_area_length,
                    (width - penalty_area_width) / 2,
                    linewidth=lw,
                ),
                Line(
                    penalty_area_length,
                    (width - penalty_area_width) / 2,
                    penalty_area_length,
                    (width + penalty_area_width) / 2,
                    linewidth=lw,
                ),
                Line(
                    penalty_area_length,
                    (width + penalty_area_width) / 2,
                    0,
                    (width + penalty_area_width) / 2,
                    linewidth=lw,
                ),
                # Right penalty area
                Line(
                    length,
                    (width - penalty_area_width) / 2,
                    length - penalty_area_length,
                    (width - penalty_area_width) / 2,
                    linewidth=lw,
                ),
                Line(
                    length - penalty_area_length,
                    (width - penalty_area_width) / 2,
                    length - penalty_area_length,
                    (width + penalty_area_width) / 2,
                    linewidth=lw,
                ),
                Line(
                    length - penalty_area_length,
                    (width + penalty_area_width) / 2,
                    length,
                    (width + penalty_area_width) / 2,
                    linewidth=lw,
                ),
            ]
        )

        # Goal areas
        self.elements.extend(
            [
                # Left goal area
                Line(
                    0,
                    (width - goal_area_width) / 2,
                    goal_area_length,
                    (width - goal_area_width) / 2,
                    linewidth=lw,
                ),
                Line(
                    goal_area_length,
                    (width - goal_area_width) / 2,
                    goal_area_length,
                    (width + goal_area_width) / 2,
                    linewidth=lw,
                ),
                Line(
                    goal_area_length,
                    (width + goal_area_width) / 2,
                    0,
                    (width + goal_area_width) / 2,
                    linewidth=lw,
                ),
                # Right goal area
                Line(
                    length,
                    (width - goal_area_width) / 2,
                    length - goal_area_length,
                    (width - goal_area_width) / 2,
                    linewidth=lw,
                ),
                Line(
                    length - goal_area_length,
                    (width - goal_area_width) / 2,
                    length - goal_area_length,
                    (width + goal_area_width) / 2,
                    linewidth=lw,
                ),
                Line(
                    length - goal_area_length,
                    (width + goal_area_width) / 2,
                    length,
                    (width + goal_area_width) / 2,
                    linewidth=lw,
                ),
            ]
        )

        # Penalty spots
        self.elements.extend(
            [
                Circle(
                    penalty_area_length + 11, width / 2, 0.1, linewidth=lw, fill=True
                ),  # Left penalty spot
                Circle(
                    length - penalty_area_length - 11,
                    width / 2,
                    0.1,
                    linewidth=lw,
                    fill=True,
                ),  # Right penalty spot
            ]
        )

        # Corner arcs
        self.elements.extend(
            [
                Arc(
                    0,
                    0,
                    2 * d["corner_arc_radius"],
                    2 * d["corner_arc_radius"],
                    angle=0,
                    theta1=0,
                    theta2=90,
                    linewidth=lw,
                ),
                Arc(
                    length,
                    0,
                    2 * d["corner_arc_radius"],
                    2 * d["corner_arc_radius"],
                    angle=270,
                    theta1=0,
                    theta2=90,
                    linewidth=lw,
                ),
                Arc(
                    0,
                    width,
                    2 * d["corner_arc_radius"],
                    2 * d["corner_arc_radius"],
                    angle=90,
                    theta1=0,
                    theta2=90,
                    linewidth=lw,
                ),
                Arc(
                    length,
                    width,
                    2 * d["corner_arc_radius"],
                    2 * d["corner_arc_radius"],
                    angle=180,
                    theta1=0,
                    theta2=90,
                    linewidth=lw,
                ),
            ]
        )
