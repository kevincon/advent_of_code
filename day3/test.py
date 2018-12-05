import collections
import itertools
import os
import pathlib
import pytest
import re
import typing


class LineSegment(typing.NamedTuple):
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length

    def intersect(self, other: 'LineSegment') -> typing.Optional['LineSegment']:
        first, second = sorted([self, other], key=lambda ls: ls.start)
        if second.start >= first.end:
            return None
        return LineSegment(start=second.start, length=(min(first.end, second.end) - second.start))


def test_line_segment_intersect():
    assert LineSegment(1, 4).intersect(LineSegment(2, 5)) == LineSegment(2, 3)
    assert LineSegment(3, 5).intersect(LineSegment(1, 4)) == LineSegment(3, 2)
    assert LineSegment(1, 4).intersect(LineSegment(2, 2)) == LineSegment(2, 2)
    assert LineSegment(1, 2).intersect(LineSegment(4, 2)) is None
    assert LineSegment(2, 2).intersect(LineSegment(4, 2)) is None


class Rectangle(typing.NamedTuple):
    x: int
    y: int
    width: int
    height: int

    def x_dimension_line_segment(self) -> LineSegment:
        return LineSegment(start=self.x, length=self.width)

    def y_dimension_line_segment(self) -> LineSegment:
        return LineSegment(start=self.y, length=self.height)

    def intersect(self, other: 'Rectangle') -> typing.Optional['Rectangle']:
        x_dimension_intersection = self.x_dimension_line_segment().intersect(other.x_dimension_line_segment())
        y_dimension_intersection = self.y_dimension_line_segment().intersect(other.y_dimension_line_segment())

        if None in [x_dimension_intersection, y_dimension_intersection]:
            return None

        return Rectangle(x=x_dimension_intersection.start, y=y_dimension_intersection.start,
                         width=x_dimension_intersection.length, height=y_dimension_intersection.length)

    def coordinate_iterator(self) -> typing.Iterator[typing.Tuple[int, int]]:
        for x in range(self.x, self.x + self.width):
            for y in range(self.y, self.y + self.height):
                yield x, y


def test_rectangle_intersect():
    assert Rectangle(0, 0, 100, 100).intersect(Rectangle(25, 25, 50, 50)) == Rectangle(25, 25, 50, 50)
    assert Rectangle(10, 10, 10, 10).intersect(Rectangle(15, 10, 10, 10)) == Rectangle(15, 10, 5, 10)
    assert Rectangle(10, 10, 10, 10).intersect(Rectangle(20, 10, 10, 10)) is None


class Claim(typing.NamedTuple):
    id: int
    rect: Rectangle


def claim_from_string(s: str) -> Claim:
    pattern = r'#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<width>\d+)x(?P<height>\d+)'
    match = re.match(pattern, s)
    return Claim(id=int(match.group('id')),
                 rect=Rectangle(x=int(match.group('x')),
                                y=int(match.group('y')),
                                width=int(match.group('width')),
                                height=int(match.group('height'))
                                )
                 )


def test_claim_from_string():
    assert claim_from_string('#1 @ 1,3: 4x4') == Claim(id=1, rect=Rectangle(1, 3, 4, 4))
    assert claim_from_string('#4321 @ 45,83: 24x13') == Claim(id=4321, rect=Rectangle(45, 83, 24, 13))


class Bitmap:
    def __init__(self, width: int, height: int):
        self._map = [[False for _ in range(height)] for _ in range(width)]

    @property
    def width(self):
        return len(self._map)

    @property
    def height(self):
        return len(self._map[0])

    def _check_if_coordinate_in_bounds(self, x, y):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            raise Exception(f'({x}, {y}) is out of bitmap bounds ({self.width}, {self.height}')

    def update(self, rect: Rectangle) -> None:
        for x, y in rect.coordinate_iterator():
            self._check_if_coordinate_in_bounds(x, y)
            self._map[x][y] = True

    def total_area(self) -> int:
        flattened_map = list(itertools.chain(*self._map))
        counter = collections.Counter(flattened_map)
        return counter[True]

    def does_cover_rect(self, rect: Rectangle) -> bool:
        for x, y in rect.coordinate_iterator():
            self._check_if_coordinate_in_bounds(x, y)
            if self._map[x][y]:
                return True
        return False


def create_bitmap_for_claims(claims: typing.List[Claim]) -> Bitmap:
    result = Bitmap(width=1000, height=1000)
    for claim1, claim2 in itertools.combinations(claims, 2):
        intersection = claim1.rect.intersect(claim2.rect)
        if intersection is not None:
            result.update(intersection)
    return result


def calculate_area_common_to_two_or_more_claims(claims: typing.List[Claim]) -> int:
    return create_bitmap_for_claims(claims).total_area()


def claims_from_claim_strings(claim_strings: typing.List[str]) -> typing.List[Claim]:
    return [claim_from_string(s) for s in claim_strings]


def calculate_area_common_to_two_or_more_claim_strings(claim_strings: typing.List[str]) -> int:
    return calculate_area_common_to_two_or_more_claims(claims_from_claim_strings(claim_strings))


def test_part1_example():
    example = [
        '#1 @ 1,3: 4x4',
        '#2 @ 3,1: 4x4',
        '#3 @ 5,5: 2x2',
    ]
    assert calculate_area_common_to_two_or_more_claim_strings(example) == 4


@pytest.fixture
def input_file_lines():
    module_dir = os.path.dirname(os.path.realpath(__file__))
    with pathlib.Path(module_dir, 'input.txt').open() as f:
        yield f.read().splitlines()


def test_part1_answer(input_file_lines):
    assert calculate_area_common_to_two_or_more_claim_strings(input_file_lines) == 103482


def get_first_uncovered_claim_in_claim_strings(claim_strings: typing.List[str]) -> typing.Optional[Claim]:
    claims = claims_from_claim_strings(claim_strings)
    bitmap = create_bitmap_for_claims(claims)
    for claim in claims:
        if not bitmap.does_cover_rect(claim.rect):
            return claim
    return None


def test_part2_answer(input_file_lines):
    assert get_first_uncovered_claim_in_claim_strings(input_file_lines).id == 686
