import functools
import operator
import typing

import pytest


@pytest.fixture()
def example_map() -> typing.List[str]:
    return [
        "..##.......",
        "#...#...#..",
        ".#....#..#.",
        "..#.#...#.#",
        ".#...##..#.",
        "..#.##.....",
        ".#.#.#....#",
        ".#........#",
        "#.##...#...",
        "#...##....#",
        ".#..#...#.#",
    ]


def count_trees_encountered(map: typing.List[str], dx: int, dy: int) -> int:
    cursor_x = 0
    cursor_y = 0
    num_trees_counted = 0

    while cursor_y < len(map):
        if map[cursor_y][cursor_x] == "#":
            num_trees_counted += 1
        cursor_y += dy
        cursor_x = (cursor_x + dx) % len(map[0])

    return num_trees_counted


def test_part1_example(example_map: typing.List[str]) -> None:
    assert count_trees_encountered(example_map, 3, 1) == 7


@pytest.fixture()
def input_map(input_file_parser) -> typing.List[str]:
    return input_file_parser("input.txt")


def test_part1_answer(input_map: typing.List[str]):
    assert count_trees_encountered(input_map, 3, 1) == 218


@pytest.fixture()
def part2_slopes() -> typing.List[typing.Tuple[int, int]]:
    return [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]


def test_part2_example(example_map: typing.List[str], part2_slopes: typing.List[typing.Tuple[int, int]]) -> None:
    assert (
        functools.reduce(
            operator.mul, map(lambda slope: count_trees_encountered(example_map, slope[0], slope[1]), part2_slopes)
        )
        == 336
    )


def test_part2_answer(input_map: typing.List[str], part2_slopes: typing.List[typing.Tuple[int, int]]) -> None:
    assert (
        functools.reduce(
            operator.mul, map(lambda slope: count_trees_encountered(input_map, slope[0], slope[1]), part2_slopes)
        )
        == 3847183340
    )
