import itertools
import os
import pathlib
import typing


def calculate_frequency_sequence(drift_sequence: typing.Iterable[int]) -> typing.List[int]:
    return list(itertools.accumulate(drift_sequence))


def test_calculate_frequency_sequence():
    assert calculate_frequency_sequence([7, 7, -2, -7, -4]) == [7, 14, 12, 5, 1]


def find_first_duplicate_frequency(frequency_sequence: typing.Iterable[int]) -> typing.Optional[int]:
    seen_frequencies = set()
    for frequency in frequency_sequence:
        if frequency in seen_frequencies:
            return frequency
        seen_frequencies.add(frequency)
    return None


def test_find_first_duplicate_frequency():
    assert find_first_duplicate_frequency([0, 1, 0]) == 0
    assert find_first_duplicate_frequency([2, 5, 3, 1, 0, -2, -4, 3]) == 3
    assert find_first_duplicate_frequency([7, 3, 1]) is None


def find_first_duplicate_frequency_in_repeating_drift_sequence(drift_sequence: typing.Iterable[int]) -> int:
    """https://adventofcode.com/2018/day/1#part2"""
    frequency_sequence = calculate_frequency_sequence(drift_sequence)

    duplicate_frequency = find_first_duplicate_frequency(itertools.chain([0], frequency_sequence))
    if duplicate_frequency is not None:
        return duplicate_frequency

    *_, last_frequency = frequency_sequence

    enumerated_frequency_sequence_pairs = list(itertools.combinations(enumerate(frequency_sequence), 2))
    differences = map(lambda pair: pair[0][1] - pair[1][1], enumerated_frequency_sequence_pairs)
    enumerated_pairs_with_differences = zip(enumerated_frequency_sequence_pairs, differences)
    only_multiples_of_last_frequency = filter(
        lambda pair_with_diff: pair_with_diff[1] % last_frequency == 0, enumerated_pairs_with_differences
    )

    def get_position_of_value_that_will_become_duplicate(pair_with_diff):
        enumerated_pair, diff = pair_with_diff
        comparison_function = min if last_frequency > 0 else max
        return comparison_function(enumerated_pair, key=lambda enumerated_value: enumerated_value[1])[0]

    sorted_by_position_of_value_that_will_become_duplicate = sorted(
        only_multiples_of_last_frequency, key=get_position_of_value_that_will_become_duplicate
    )
    smallest_magnitude_diff_enumerated_pair, _ = min(
        sorted_by_position_of_value_that_will_become_duplicate, key=lambda pair_with_diff: abs(pair_with_diff[1])
    )
    _, smallest_magnitude_diff_pair = zip(*smallest_magnitude_diff_enumerated_pair)
    comparision_function = max if last_frequency > 0 else min
    return comparision_function(smallest_magnitude_diff_pair)


def test_find_first_duplicate_frequency_in_repeating_drift_sequence():
    # 3, 6, 8, 4
    # 7, 10, 12, 8, ...
    assert find_first_duplicate_frequency_in_repeating_drift_sequence([3, 3, 2, -4]) == 8

    # = -6, -2, -1, -4, -3
    # = -9, -5, -4, ...
    assert find_first_duplicate_frequency_in_repeating_drift_sequence([-6, 4, 1, -3, 1]) == -4


def test_example1():
    assert find_first_duplicate_frequency_in_repeating_drift_sequence([1, -1]) == 0


def test_example2():
    # 3, 6, 10, 8, 4
    # 7, 10, ...
    assert find_first_duplicate_frequency_in_repeating_drift_sequence([3, 3, 4, -2, -4]) == 10


def test_example3():
    # -6, -3, 5, 10, 4
    # -2, 1, 9, 14, 8
    # 2, 5, ...
    assert find_first_duplicate_frequency_in_repeating_drift_sequence([-6, 3, 8, 5, -6]) == 5


def test_example4():
    # 7, 14, 12, 5, 1
    # 8, 15, 13, 6, 2
    # 9, 16, 14, ...
    assert find_first_duplicate_frequency_in_repeating_drift_sequence([7, 7, -2, -7, -4]) == 14


def test_answer():
    module_dir = os.path.dirname(os.path.realpath(__file__))
    with pathlib.Path(module_dir, "input.txt").open() as f:
        assert find_first_duplicate_frequency_in_repeating_drift_sequence(map(int, f.readlines())) == 82516
