import collections
import os
import pathlib
import typing


def calculate_checksum(box_ids: typing.Iterable[str]) -> int:
    """https://adventofcode.com/2018/day/2"""
    num_ids_with_two_counts = 0
    num_ids_with_three_counts = 0
    for box_id in box_ids:
        counts_counter = collections.Counter(collections.Counter(box_id).values())
        if counts_counter[2] > 0:
            num_ids_with_two_counts += 1
        if counts_counter[3] > 0:
            num_ids_with_three_counts += 1
    return num_ids_with_two_counts * num_ids_with_three_counts


def test_example():
    assert (
        calculate_checksum(
            [
                "abcdef",
                "bababc",
                "abbcde",
                "abcccd",
                "aabcdd",
                "abcdee",
                "ababab",
            ]
        )
        == 12
    )


def test_answer():
    module_dir = os.path.dirname(os.path.realpath(__file__))
    with pathlib.Path(module_dir, "input.txt").open() as f:
        assert calculate_checksum(f.readlines()) == 5368
