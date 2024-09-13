import os
import pytest
from PIL import Image  # Pillow library for opening and inspecting image files
from pathlib import Path
from grafte.chart import Bar

import csv
from io import StringIO, BytesIO


@pytest.fixture
def ez_data():
    return [["al", 1], ["bob", 2]]


@pytest.fixture
def input_csv_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "input.csv"
    p.write_text(
        """
name,age
Alice,42
Bob,9
Chaz,101
""".strip()
    )
    return p


@pytest.mark.alpha
def test_chart_from_csv(input_csv_file):
    with open(input_csv_file, "r") as i:
        data = list(csv.DictReader(i))

    cx = Bar(data, xvar="name", yvar="age")
    assert cx.data.X == ["Alice", "Bob", "Chaz"]
    assert cx.data.Y == ["42", "9", "101"]


def test_chart_save_as_file(tmp_path):
    test_image_path = tmp_path / "bar.png"

    cx = Bar(ez_data, canvas={"width": 200, "height": 100})

    cx.save(test_image_path)
    assert test_image_path.exists(), "The image file was not created."
    with Image.open(test_image_path) as img:
        # The expected dimensions are width/height in pixels based on DPI
        expected_width = cx.canvas.width
        expected_height = cx.canvas.height

        assert (
            img.width == expected_width
        ), f"Expected width: {expected_width}, but got {img.width}"
        assert (
            img.height == expected_height
        ), f"Expected height: {expected_height}, but got {img.height}"
