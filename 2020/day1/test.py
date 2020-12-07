import typing

import pytest


@pytest.fixture()
def input_entries(input_file_parser) -> typing.Set[int]:
    return set(map(int, input_file_parser("input.txt")))


def part1(entries: typing.Set[int], target_sum: int) -> typing.Optional[int]:
    for entry in entries:
        entry_mate_candidate = target_sum - entry
        if entry_mate_candidate in entries:
            return entry * entry_mate_candidate
    return None


def test_part1_answer(input_entries: typing.Set[int]) -> None:
    assert part1(input_entries, target_sum=2020) == 858496


def part2(entries: typing.Set[int]) -> typing.Optional[int]:
    entry_set = set(entries)
    for entry in entry_set:
        remainder = 2020 - entry
        result = part1(entries - set([entry]), target_sum=remainder)
        if result is not None:
            return result * entry
    return None


def test_part2_answer(input_entries: typing.Set[int]) -> None:
    assert part2(input_entries) == 263819430
