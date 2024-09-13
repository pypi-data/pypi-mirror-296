import pytest
from collections import namedtuple

# from click.testing import CliRunner
from grafte.lib.canvas import CanvasConfig


def test_canvas_config_inits_with_namedtuple():
    c = CanvasConfig(width=500, height=700, dpi=100)
    assert c.dpi == 100


def test_canvas_matplotlib_config_obj():
    c = CanvasConfig({"width": 500, "height": 700, "dpi": 100})
    d = c.to_matplotlib_config()
    assert d["dpi"] == 100
    assert d["figsize"] == (5, 7)
