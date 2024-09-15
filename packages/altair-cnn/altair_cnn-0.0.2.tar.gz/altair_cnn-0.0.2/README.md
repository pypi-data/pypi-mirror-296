
# altair_cnn

A custom theme for Python's Altair statistical visualization library, inspired by CNN's design.

## Overview

This package provides a custom Altair theme named `altair_cnn` that you can use to style your Altair charts with CNN's visual design. The theme includes custom color schemes and configuration options tailored to align with CNN's branding.

## Directory Structure

```
altair_cnn/
│
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── altair_cnn
│   ├── __init__.py
│   └── altair_cnn.py
├── notebook.ipynb
└── setup.py
```

- **LICENSE**: The license under which this package is distributed.
- **Pipfile** and **Pipfile.lock**: For managing dependencies with `pipenv`.
- **README.md**: This file, containing package documentation.
- **altair_cnn/**: Directory containing the theme implementation.
- **notebook.ipynb**: A Jupyter notebook demonstrating how to use the theme with sample charts.
- **setup.py**: Configuration file for building and installing the package.

## Installation

### Requirements

- Python 3.6 or higher
- Altair 5.4.0 or higher

### Installing the Package

You can install the package from PyPI (if published) or directly from your local repository.

#### From PyPI

To install from PyPI, use:

```bash
pip install altair_cnn
```

#### From Local Repository

To install from a local clone of this repository:

1. Clone the repository:

   ```bash
   git clone https://github.com/turnercode/altair-cnn.git
   cd altair-cnn
   ```

2. Install the package locally:

   ```bash
   pip install .
   ```

## Usage

Once installed, you can register and enable the `altair_cnn` theme in your Python scripts or Jupyter notebooks:

```python
import altair as alt
from altair_cnn import theme

# Register and enable the theme
alt.themes.register('altair_cnn', theme)
alt.themes.enable('altair_cnn')

# Create a chart using the theme
source = alt.data.iowa_electricity()

alt.Chart(source, title="Iowa's renewable energy boom").mark_area().encode(
    x=alt.X(
        "year:T",
        title=" "
    ),
    y=alt.Y(
        "net_generation:Q",
        stack="normalize",
        title="Share of energy production, by source",
        axis=alt.Axis(format=".0%", tickCount=5),
    ),
    color=alt.Color(
        "source:N",
        legend=alt.Legend(title=""),
    )
)
```

## Development

### Building the Package

To build the package for distribution, run the following command from the root directory:

```bash
python setup.py sdist bdist_wheel
```

This command will create a `dist/` directory containing the distribution files.

### Publishing to PyPI

To publish the package to PyPI, you will need an account on [PyPI](https://pypi.org/). Follow these steps:

1. Ensure you have `twine` installed:

   ```bash
   pip install twine
   ```

2. Upload the package to PyPI:

   ```bash
   twine upload dist/*
   ```

Follow the prompts to enter your PyPI username and password.

## Example Usage in Jupyter Notebook

Included in this repository is a Jupyter notebook (`notebook.ipynb`) with examples of using the `altair_cnn` theme. You can open this notebook with Jupyter to see sample visualizations and experiment with the theme.

To run the notebook:

```bash
jupyter notebook notebook.ipynb
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to contribute to this project by submitting issues or pull requests!
