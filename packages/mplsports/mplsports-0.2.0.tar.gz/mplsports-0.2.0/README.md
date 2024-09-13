# mplsports (WIP)

A highly customizable library for plotting sports fields and courts using Matplotlib.

> Work in progress! Still doesn't work yet!

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [Plotting a Soccer Pitch](#plotting-a-soccer-pitch)
  - [Plotting Other Sports](#plotting-other-sports)
- [Customization](#customization)
- [Adding Custom Dimensions](#adding-custom-dimensions)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`mplsports` is a Python library designed for plotting various sports fields and courts using Matplotlib. It provides high customizability, allowing users to adjust dimensions, colors, line styles, and more. The library supports multiple sports, including soccer, basketball, tennis, handball, and volleyball, with an extensible architecture that makes it easy to add new sports.

---

## Features

- **Multiple Sports Support**: Plot pitches for soccer, basketball, tennis, handball, volleyball, and more.
- **High Customizability**: Customize colors, line styles, dimensions, units, and padding.
- **Extensible Architecture**: Easily add support for additional sports.
- **Standard and Custom Dimensions**: Use standard dimensions or provide your own.
- **Future-Proof**: Designed to support both 2D and upcoming 3D plotting capabilities.

---

## Installation

Install `mplsports` using pip:

```bash
pip install mplsports
```

---

## Quick Start

`mplsports` provides a flexible API that accommodates various terms for sports playing areas. You can use `Pitch`, `Court`, `Field`, `Ground`, or even `Thing` interchangeably to create your sports visualizations.　 This flexibility allows you to use terminology you're comfortable with while maintaining full access to the library's features.

```python
from mplsports import Pitch, Court, Field, Ground, Thing
import matplotlib.pyplot as plt

# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(20, 20))
Flatten the 2D array of axes for easier indexing
axs = axs.flatten()

# soccer
soccer_pitch = Pitch(sport="soccer", axis=True, tick=True)
soccer_pitch.draw(ax=axs[0])
axs[0].set_title("Soccer Pitch")

# Basketball
basketball_court = Court(sport="basketball", axis=True, tick=True)
basketball_court.draw(ax=axs[1])
axs[1].set_title("Basketball Court")

# Tennis
tennis_court = Field(sport="tennis", axis=True, tick=True)
tennis_court.draw(ax=axs[2])
axs[2].set_title("Tennis Court")

# Handball
handball_court = Ground(sport="handball", axis=True, tick=True)
handball_court.draw(ax=axs[3])
axs[3].set_title("Handball Court")

# Adjust the layout and display the plot
plt.tight_layout()
plt.show()
```

### Plotting a Soccer Pitch

```python
from mplsports.pitch.soccer import SoccerPitch
import matplotlib.pyplot as plt

# Create a soccer pitch instance
pitch = SoccerPitch(
    pitch_color='#a8bc95',
    line_color='white',
    line_alpha=0.8,
    linewidth=2,
    linestyle='-',
    axis=True,
    tick=False,
    label=False
)

# Draw the pitch
ax = pitch.draw()

# Show the plot
plt.show()
```

### Plotting Other Sports

```python
from mplsports.pitch.basketball import BasketballCourt

# Create a basketball court instance
court = BasketballCourt(
    pitch_color='#f0f0f0',
    line_color='black',
    linewidth=2,
    half=False
)

# Draw the court
ax = court.draw()

plt.show()
```

---

## Customization

`mplsports` allows extensive customization through various parameters:

- **Colors**: `pitch_color`, `line_color`
- **Line Styles**: `linewidth`, `linestyle`, `line_alpha`, `line_zorder`
- **Axis Settings**: `axis`, `tick`, `label`
- **Padding**: `pad_left`, `pad_right`, `pad_bottom`, `pad_top`
- **Dimension Configurations**: Use predefined pitch types or pass custom dimensions.

### Example: Customizing a Tennis Court

```python
from mplsports.pitch.tennis import TennisCourt

court = TennisCourt(
    pitch_color='#008000',
    line_color='white',
    linewidth=2,
    line_zorder=1,
    axis=True,
    tick=False,
    label=False,
    pad_left=2,
    pad_right=2,
    pad_bottom=1,
    pad_top=1
)

ax = court.draw()
plt.show()
```

---

## Adding Custom Dimensions

You can use custom dimensions by creating a dictionary of dimensions or providing a custom YAML file.

### Using a Custom Dimensions Dictionary

```python
custom_dimensions = {
    'length': 120.0,
    'width': 75.0,
    'line_width': 0.12,
    'penalty_area_length': 18.0,
    'penalty_area_width': 44.0,
    'goal_area_length': 6.0,
    'goal_area_width': 20.0,
    'center_circle_radius': 10.0,
    'corner_arc_radius': 1.0
}

pitch = SoccerPitch(config=custom_dimensions)
ax = pitch.draw()
plt.show()
```

### Using a Custom YAML Configuration

1. Create a YAML file with your custom dimensions (e.g., `my_custom_pitch.yaml`).

```yaml
length: 120.0
width: 75.0
line_width: 0.12
penalty_area_length: 18.0
penalty_area_width: 44.0
goal_area_length: 6.0
goal_area_width: 20.0
center_circle_radius: 10.0
corner_arc_radius: 1.0
```

2. Load the configuration and pass it to the pitch class.

```python
import yaml

with open('my_custom_pitch.yaml', 'r') as f:
    custom_config = yaml.safe_load(f)

pitch = SoccerPitch(config=custom_config)
ax = pitch.draw()
plt.show()
```

---

## Roadmap

- Verify pitches for each sport:
  - Soccer
  - Basketball
  - Tennis
  - Handball
  - Volleyball
- Add documentation
- Add 3D plots for each sport:
  - Soccer
  - Basketball
  - Tennis
  - Handball
  - Volleyball

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bugfix.
3. Write tests for your changes.
4. Submit a pull request with a detailed description.

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/yourusername/mplsports/blob/main/LICENSE) file for details.

---

## Acknowledgements

Special thanks to the community for their contributions and support. This project was heavily influenced by:

- [mplsoccer](https://github.com/andrewRowlinson/mplsoccer)
- [mplbasketball](https://github.com/mlsedigital/mplbasketball)

I initially struggled to plot a handball court for my research and thought it would be useful for myself and colleagues to have a simple, yet extensible version of these two repositories.
