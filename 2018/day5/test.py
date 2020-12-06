import os
import pathlib
import pytest


@pytest.fixture
def example():
    yield "dabAcCaCBAcCcaDA"


@pytest.fixture
def input_file_string():
    module_dir = os.path.dirname(os.path.realpath(__file__))
    with pathlib.Path(module_dir, "input.txt").open() as f:
        yield f.read().strip()


def do_units_react(unit1: str, unit2: str) -> bool:
    return (unit1.lower() == unit2.lower()) and (unit1 != unit2)


def test_do_units_react():
    assert do_units_react("a", "A") is True
    assert do_units_react("a", "a") is False
    assert do_units_react("a", "b") is False
    assert do_units_react("a", "B") is False


def simplify(units_left: str) -> str:
    result = ""

    while True:
        # Take the first two units from the units left to process
        unit1, unit2, units_left = units_left[0:1], units_left[1:2], units_left[2:]
        if unit1 == "":
            return result
        if unit2 == "":
            return result + unit1

        # If the two units react, pop the last unit from the result and add it to the front of the units left to process
        if do_units_react(unit1, unit2):
            popped, result = result[-1:], result[:-1]
            units_left = popped + units_left
        else:
            # Otherwise add the first unit to the end of the result and continue processing from the second unit
            result += unit1
            units_left = unit2 + units_left


def test_simplify():
    assert simplify("a") == "a"
    assert simplify("B") == "B"
    assert simplify("aA") == ""
    assert simplify("Bb") == ""
    assert simplify("aBA") == "aBA"
    assert simplify("aaA") == "a"
    assert simplify("AaBb") == ""
    assert simplify("") == ""
    assert simplify("aBbA") == ""
    assert simplify("bBa") == "a"


def test_part1_example(example):
    assert simplify(example) == "dabCBAcaDA"


def test_part1_answer(input_file_string):
    """https://adventofcode.com/2018/day/5"""
    simplified = simplify(input_file_string)
    assert len(simplified) == 11042


def find_shortest_length_polymer_from_removing_one_unit_type(units: str) -> int:
    """https://adventofcode.com/2018/day/5#part2"""
    unit_set = set(units.lower())

    simplified_lengths = []

    for unit_to_remove in unit_set:
        filtered_units = "".join(list(filter(lambda x: x.lower() != unit_to_remove, units)))
        simplified = simplify(filtered_units)
        simplified_lengths.append(len(simplified))

    return min(simplified_lengths)


def test_part2_example(example):
    assert find_shortest_length_polymer_from_removing_one_unit_type(example) == 4


def test_part2_answer(input_file_string):
    assert find_shortest_length_polymer_from_removing_one_unit_type(input_file_string) == 6872
