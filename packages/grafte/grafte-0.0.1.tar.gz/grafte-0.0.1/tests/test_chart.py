import pytest
from grafte.chart import Bar


def test_basic_chart():
    data = [["al", 1], ["bob", 2]]
    cx = Bar(data, canvas={"width": 200, "height": 100})

    assert cx.canvas.width == 200
    assert cx.canvas.height == 100
