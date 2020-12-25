import collections
import typing

import pytest


@pytest.fixture()
def input_descriptions(input_file_parser) -> typing.List[str]:
    return input_file_parser("input.txt")


def is_password_description_valid_using_part1_interpretation(description: str) -> bool:
    policy, password = description.split(": ")

    min_max, constrained_char = policy.split(" ")

    min, max = map(int, min_max.split("-"))

    char_counter = collections.Counter(password)
    return min <= char_counter[constrained_char] <= max


def count_valid_part1_password_descriptions(descriptions: typing.List[str]) -> int:
    return len(list(filter(is_password_description_valid_using_part1_interpretation, descriptions)))


@pytest.fixture()
def example_password_descriptions() -> typing.List[str]:
    return [
        "1-3 a: abcde",
        "1-3 b: cdefg",
        "2-9 c: ccccccccc",
    ]


def test_part1_example(example_password_descriptions: typing.List[str]) -> None:
    assert count_valid_part1_password_descriptions(example_password_descriptions) == 2


def test_part1_answer(input_descriptions: typing.List[str]) -> None:
    assert count_valid_part1_password_descriptions(input_descriptions) == 393


def is_password_description_valid_using_part2_interpretation(description: str) -> bool:
    policy, password = description.split(": ")

    first_last, constrained_char = policy.split(" ")

    first, last = map(int, first_last.split("-"))

    return (password[first - 1] == constrained_char) ^ (password[last - 1] == constrained_char)


def count_valid_part2_password_descriptions(descriptions: typing.List[str]) -> int:
    return len(list(filter(is_password_description_valid_using_part2_interpretation, descriptions)))


def test_part2_example(example_password_descriptions: typing.List[str]) -> None:
    assert count_valid_part2_password_descriptions(example_password_descriptions) == 1


def test_part2_answer(input_descriptions: typing.List[str]) -> None:
    assert count_valid_part2_password_descriptions(input_descriptions) == 690
