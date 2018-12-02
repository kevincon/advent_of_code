import os
import pathlib
import typing


def calibrate_frequency_drift(drift_sequence: typing.Iterable[int])-> int:
    """https://adventofcode.com/2018/day/1"""
    return sum(drift_sequence)


def test_example1():
    assert 3 == calibrate_frequency_drift([1, 1, 1])


def test_example2():
    assert 0 == calibrate_frequency_drift([1, 1, -2])


def test_example3():
    assert -6 == calibrate_frequency_drift([-1, -2, -3])


def test_answer():
    module_dir = os.path.dirname(os.path.realpath(__file__))
    with pathlib.Path(module_dir, 'input.txt').open() as f:
        assert 578 == calibrate_frequency_drift(map(int, f.readlines()))
