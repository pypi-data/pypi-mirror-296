import pytest

# from click.testing import CliRunner
from grafte.lib.data import DataObj


def test_unlabeled_dataobj():
    d = DataObj([["a", 1], ["b", 5]])
    assert d.xvar == 0
    assert d.yvar == 1
    assert d.cvar == None
    assert d.is_multi_series is False

def test_specific_dataobj():
    d = DataObj(
        [
            {"id": "a", "amt": 6},
            {"id": "b", "amt": 7},
        ],
        xvar="id",
        yvar="amt",
    )

    assert d.xvar == "id"
    assert d.yvar == "amt"
    assert d.cvar == None
    assert d.X == ["a", "b"]
    assert d.Y == [6, 7]
    assert d.is_multi_series is False

def test_multiseries_dataobj():
    d = DataObj(
        [

            {"id": "a", "amt": 2, "region": 'SE'},
            {"id": "a", "amt": 6, "region": 'NW'},
            {"id": "b", "amt": 7, "region": 'NW'},
            {"id": "b", "amt": 5, "region": 'SE'},

        ],
        xvar="id",
        yvar="amt",
        cvar='region'
    )

    assert d.xvar == "id"
    assert d.yvar == "amt"
    assert d.cvar == 'region'
    assert d.X == ["a", "a", "b", "b"]
    assert d.Y == [2, 6, 7, 5]
    assert d.C == ['SE', 'NW',   'NW',  'SE',]
    assert d.c_labels == ['SE', 'NW'], 'c_labels is supposed to preserve order of series as they appeared in original data'
    assert d.is_multi_series is True
