# geometry/line.py
from dataclasses import dataclass
import matplotlib.lines as mlines


@dataclass
class Line:
    x_start: float
    y_start: float
    x_end: float
    y_end: float
    color: str = "black"
    alpha: float = 1.0
    linewidth: float = 2
    linestyle: str = "-"
    zorder: float = 0.9

    def draw(self, ax):
        line = mlines.Line2D(
            [self.x_start, self.x_end],
            [self.y_start, self.y_end],
            color=self.color,
            alpha=self.alpha,
            linewidth=self.linewidth,
            linestyle=self.linestyle,
            zorder=self.zorder,
        )
        ax.add_line(line)

    def translate(self, dx, dy):
        self.x_start += dx
        self.y_start += dy
        self.x_end += dx
        self.y_end += dy

    def rotate(self, angle, origin=(0, 0)):
        # Implement rotation logic if needed
        pass
