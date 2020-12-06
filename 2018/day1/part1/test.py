import os
import pathlib
import typing


def calibrate_frequency_drift(drift_sequence: typing.Iterable[int]) -> int:
    """https://adventofcode.com/2018/day/1"""
    return sum(drift_sequence)


def test_example1():
    assert calibrate_frequency_drift([1, 1, 1]) == 3


def test_example2():
    assert calibrate_frequency_drift([1, 1, -2]) == 0


def test_example3():
    assert calibrate_frequency_drift([-1, -2, -3]) == -6


def test_answer():
    module_dir = os.path.dirname(os.path.realpath(__file__))
    with pathlib.Path(module_dir, "input.txt").open() as f:
        assert calibrate_frequency_drift(map(int, f.readlines())) == 578
