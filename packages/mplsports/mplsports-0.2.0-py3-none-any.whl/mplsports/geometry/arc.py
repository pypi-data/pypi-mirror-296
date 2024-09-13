# geometry/arc.py
from dataclasses import dataclass
import matplotlib.patches as mpatches


@dataclass
class Arc:
    center_x: float
    center_y: float
    width: float
    height: float
    angle: float
    theta1: float
    theta2: float
    color: str = "black"
    alpha: float = 1.0  # Added alpha
    linewidth: float = 2
    linestyle: str = "-"  # Added linestyle
    zorder: float = 0.9  # Added zorder

    def draw(self, ax):
        arc = mpatches.Arc(
            (self.center_x, self.center_y),
            self.width,
            self.height,
            angle=self.angle,
            theta1=self.theta1,
            theta2=self.theta2,
            edgecolor=self.color,
            linewidth=self.linewidth,
            alpha=self.alpha,  # Added alpha
            linestyle=self.linestyle,  # Added linestyle
            zorder=self.zorder,  # Added zorder
        )
        ax.add_patch(arc)

    def translate(self, dx, dy):
        self.center_x += dx
        self.center_y += dy

    def rotate(self, angle, origin=(0, 0)):
        # Implement rotation logic if needed
        pass
