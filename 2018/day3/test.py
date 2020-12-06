import itertools
import os
import pathlib
import pytest
import re
import typing


class Rectangle(typing.NamedTuple):
    x: int
    y: int
    width: int
    height: int

    def coordinate_iterator(self) -> typing.Iterator[typing.Tuple[int, int]]:
        for x in range(self.x, self.x + self.width):
            for y in range(self.y, self.y + self.height):
                yield x, y


class Claim(typing.NamedTuple):
    id: int
    rect: Rectangle


def claim_from_string(s: str) -> Claim:
    pattern = r"#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<width>\d+)x(?P<height>\d+)"
    match = re.match(pattern, s)
    assert match is not None
    return Claim(
        id=int(match.group("id")),
        rect=Rectangle(
            x=int(match.group("x")),
            y=int(match.group("y")),
            width=int(match.group("width")),
            height=int(match.group("height")),
        ),
    )


def test_claim_from_string():
    assert claim_from_string("#1 @ 1,3: 4x4") == Claim(id=1, rect=Rectangle(1, 3, 4, 4))
    assert claim_from_string("#4321 @ 45,83: 24x13") == Claim(id=4321, rect=Rectangle(45, 83, 24, 13))


class CounterMap:
    def __init__(self, width: int, height: int):
        self._map = [[0 for _ in range(height)] for _ in range(width)]

    def update(self, rect: Rectangle) -> None:
        for x, y in rect.coordinate_iterator():
            self._map[x][y] += 1

    def common_area(self) -> int:
        flattened_map = list(itertools.chain(*self._map))
        return len(list(filter(lambda x: x > 1, flattened_map)))

    def does_cover_rect(self, rect: Rectangle) -> bool:
        for x, y in rect.coordinate_iterator():
            if self._map[x][y] > 1:
                return True
        return False


def create_counter_map_for_claims(claims: typing.List[Claim]) -> CounterMap:
    result = CounterMap(width=1000, height=1000)
    for claim in claims:
        result.update(claim.rect)
    return result


def calculate_area_common_to_two_or_more_claims(claims: typing.List[Claim]) -> int:
    return create_counter_map_for_claims(claims).common_area()


def claims_from_claim_strings(claim_strings: typing.List[str]) -> typing.List[Claim]:
    return [claim_from_string(s) for s in claim_strings]


def calculate_area_common_to_two_or_more_claim_strings(claim_strings: typing.List[str]) -> int:
    """https://adventofcode.com/2018/day/3"""
    return calculate_area_common_to_two_or_more_claims(claims_from_claim_strings(claim_strings))


def test_part1_example():
    example = [
        "#1 @ 1,3: 4x4",
        "#2 @ 3,1: 4x4",
        "#3 @ 5,5: 2x2",
    ]
    assert calculate_area_common_to_two_or_more_claim_strings(example) == 4


@pytest.fixture
def input_file_lines():
    module_dir = os.path.dirname(os.path.realpath(__file__))
    with pathlib.Path(module_dir, "input.txt").open() as f:
        yield f.read().splitlines()


def test_part1_answer(input_file_lines):
    assert calculate_area_common_to_two_or_more_claim_strings(input_file_lines) == 103482


def get_first_uncovered_claim_in_claim_strings(claim_strings: typing.List[str]) -> typing.Optional[Claim]:
    """https://adventofcode.com/2018/day/3#part2"""
    claims = claims_from_claim_strings(claim_strings)
    bitmap = create_counter_map_for_claims(claims)
    for claim in claims:
        if not bitmap.does_cover_rect(claim.rect):
            return claim
    return None


def test_get_first_uncovered_claim_in_claim_strings():
    assert get_first_uncovered_claim_in_claim_strings([]) is None


def test_part2_answer(input_file_lines):
    assert get_first_uncovered_claim_in_claim_strings(input_file_lines).id == 686
