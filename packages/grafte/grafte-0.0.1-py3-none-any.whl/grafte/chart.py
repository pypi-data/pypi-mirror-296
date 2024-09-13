import matplotlib.pyplot as plt
from grafte.lib.data import DataObj
from grafte.lib.canvas import CanvasConfig
from typing import Union, List, Dict, Iterable, Optional


class Chart:
    def __init__(
        self,
        data: Iterable,
        canvas: Optional[Union[CanvasConfig, dict]] = None,
        **kwargs
    ):
        self.chart_type = "default"

        self.data = DataObj(
            data,
            xvar=kwargs.get("xvar"),
            yvar=kwargs.get("yvar"),
            cvar=kwargs.get("cvar"),
        )
        self.canvas = CanvasConfig(canvas)
        self.figure, self.ax = self._setup_canvas()

    def _setup_canvas(self):
        # Set up the canvas based on provided properties
        fig = self.canvas.config_matplotlib_figure(plt)
        ax = fig.add_subplot(111)

        return fig, ax

    def draw(self):
        self.render()
        self.show()

    def render(self):
        pass

    def show(self):
        plt.show()

    def save(self, filepath):
        """Save the chart to a file."""
        self.figure.savefig(filepath)

    def get_figure(self):
        """Return the figure object, allowing external access."""
        return self.figure

    def get_axes(self):
        """Return the axes object, allowing external access."""
        return self.ax


class Bar(Chart):
    def __init__(self, *args, **kwargs):
        self.chart_type = "bar"
        super().__init__(*args, **kwargs)

    def render(self):
        if not self.data.is_multi_series:
            x = self.data.X
            y = self.data.Y
            self.ax.bar(x, y)
        else:
            """
            TODO: multi-series grouped bar chart
            https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

            convert data structure into [{label: y_vals}]
            create an array of unique x-labels, assign x pos to them


            """
            pass

class Line(Chart):
    def __init__(self, *args, **kwargs):
        self.chart_type = "bar"
        super().__init__(*args, **kwargs)

    def render(self):
        if not self.data.is_multi_series:
            x = self.data.X
            y = self.data.Y
            self.ax.plot(x, y)
        else:
            pass


class Scatter(Chart):
    def __init__(self, *args, **kwargs):
        self.chart_type = "scatter"
        super().__init__(*args, **kwargs)

    def render(self):
        if not self.data.is_multi_series:
            x = self.data.X
            y = self.data.Y
            self.ax.scatter(x, y)
        else:
            pass
