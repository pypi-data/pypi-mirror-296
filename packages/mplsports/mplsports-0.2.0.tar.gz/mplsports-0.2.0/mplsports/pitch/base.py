# pitch/base.py
import matplotlib.pyplot as plt
import yaml
import os


class PitchBase:
    """A base class for plotting sports pitches with high customizability.

    Parameters
    ----------
    pitch_type : str, default 'standard'
        The type of pitch dimensions to use. Different sports or leagues may have different standard dimensions.
    half : bool, default False
        Whether to display only half of the pitch.
    pitch_color : str or None, default None
        The background color of the pitch. If None, defaults to Matplotlib's default axes facecolor.
    line_color : str or None, default None
        The color of the pitch lines. If None, defaults to Matplotlib's default grid color.
    line_alpha : float, default 1.0
        The transparency of the pitch lines.
    linewidth : float, default 2
        The width of the pitch lines.
    linestyle : str or tuple, default '-'
        The style of the pitch lines.
    line_zorder : float, default 0.9
        The drawing order of the pitch lines. Lower values are drawn first.
    axis : bool, default False
        Whether to display the axis spines.
    tick : bool, default False
        Whether to display the axis ticks.
    label : bool, default False
        Whether to display the axis labels.
    pad_left : float, default 0
        Padding to add to the left of the pitch.
    pad_right : float, default 0
        Padding to add to the right of the pitch.
    pad_bottom : float, default 0
        Padding to add to the bottom of the pitch.
    pad_top : float, default 0
        Padding to add to the top of the pitch.
    **kwargs : dict
        Additional keyword arguments for further customization.
    """

    def __init__(
        self,
        pitch_type="standard",
        half=False,
        pitch_color=None,
        line_color=None,
        line_alpha=1.0,
        linewidth=2,
        linestyle="-",
        line_zorder=0.9,
        axis=False,
        tick=False,
        label=False,
        pad_left=0,
        pad_right=0,
        pad_bottom=0,
        pad_top=0,
        config=None,
        **kwargs,
    ):
        self.pitch_type = pitch_type
        self.half = half
        self.pitch_color = pitch_color
        self.line_color = line_color
        self.line_alpha = line_alpha
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.line_zorder = line_zorder
        self.axis = axis
        self.tick = tick
        self.label = label
        self.pad_left = pad_left
        self.pad_right = pad_right
        self.pad_bottom = pad_bottom
        self.pad_top = pad_top
        self.elements = []
        self.dimensions = config or self._load_config()
        self.additional_params = kwargs
        self._apply_customizations()

    def _load_config(self):
        """Load pitch dimensions based on the selected sport type."""
        base_dir = os.path.join(os.path.dirname(__file__), "..", "dimensions")
        sport_type = self.sport_type
        config_filename = f"{self.pitch_type}.yaml"

        config_path = os.path.join(base_dir, sport_type, config_filename)

        print(f"Loading config from {config_path}")
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        return data

    def _apply_customizations(self):
        """Apply customizations to the pitch elements."""
        # This method can be overridden by subclasses to apply specific customizations
        pass

    def draw(self, ax=None):
        """Draw the pitch on a Matplotlib axis."""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 7))

        # Set pitch background color
        if self.pitch_color is not None:
            ax.set_facecolor(self.pitch_color)

        # Draw pitch elements
        for element in self.elements:
            element.draw(ax)

        # Set axis visibility
        if not self.axis:
            ax.axis("off")
        if not self.tick:
            ax.set_xticks([])
            ax.set_yticks([])
        if not self.label:
            ax.set_xlabel("")
            ax.set_ylabel("")

        # Set axis limits with padding
        x_min = self.dimensions["left"] - self.pad_left
        x_max = self.dimensions["right"] + self.pad_right
        y_min = self.dimensions["bottom"] - self.pad_bottom
        y_max = self.dimensions["top"] + self.pad_top

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_aspect("equal")

        return ax

    def add_element(self, element):
        """Add a custom element to the pitch."""
        self.elements.append(element)
