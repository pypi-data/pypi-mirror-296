# geometry/circle.py
from dataclasses import dataclass
import matplotlib.patches as mpatches


@dataclass
class Circle:
    center_x: float
    center_y: float
    radius: float
    color: str = "black"
    alpha: float = 1.0  # Added alpha
    linewidth: float = 2
    linestyle: str = "-"  # Added linestyle
    zorder: float = 0.9  # Added zorder
    fill: bool = False

    def draw(self, ax):
        circle = mpatches.Circle(
            (self.center_x, self.center_y),
            self.radius,
            edgecolor=self.color,
            facecolor=self.color if self.fill else "none",
            linewidth=self.linewidth,
            alpha=self.alpha,  # Added alpha
            linestyle=self.linestyle,  # Added linestyle
            zorder=self.zorder,  # Added zorder
        )
        ax.add_patch(circle)

    def translate(self, dx, dy):
        self.center_x += dx
        self.center_y += dy

    def rotate(self, angle, origin=(0, 0)):
        # Implement rotation logic if needed
        pass
