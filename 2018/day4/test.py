import collections
import datetime
import os
import pathlib
import pytest
import re
import typing

EXAMPLE_INPUT = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""


def guard_observation_sort_key_func(observation: str) -> datetime.datetime:
    match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]", observation)
    assert match is not None
    datetime_string = match.group(1)
    return datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M")


def sort_guard_observation_strings_by_timestamp(observations: typing.List[str]) -> typing.List[str]:
    return sorted(observations, key=guard_observation_sort_key_func)


def test_sort_guard_observation_strings_by_timestamp():
    # Shuffled via http://www.unit-conversion.info/texttools/shuffle-lines/
    shuffled_example_input = """[1518-11-04 00:02] Guard #99 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-03 00:24] falls asleep
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-01 00:55] wakes up
[1518-11-04 00:46] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-05 00:45] falls asleep
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-05 00:55] wakes up
"""
    assert (
        sort_guard_observation_strings_by_timestamp(shuffled_example_input.splitlines()) == EXAMPLE_INPUT.splitlines()
    )


def guard_sleep_schedules_from_strings(lines: typing.List[str]) -> typing.Dict[int, collections.Counter]:
    lines = sort_guard_observation_strings_by_timestamp(lines)

    result: typing.DefaultDict[int, collections.Counter] = collections.defaultdict(collections.Counter)

    i = 0
    while i < len(lines):
        shift_start_match = re.match(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] Guard #(?P<id>\d+) begins shift", lines[i])
        if shift_start_match is not None:
            guard_id = int(shift_start_match.group("id"))
            i += 1

        sleep_cycle_lines = "\n".join([lines[i], lines[i + 1]])
        sleep_cycle_match = re.match(
            r"\[\d{4}-\d{2}-\d{2} \d{2}:(?P<minute_asleep>\d{2})\] falls asleep\n"
            r"\[\d{4}-\d{2}-\d{2} \d{2}:(?P<minute_awake>\d{2})\] wakes up",
            sleep_cycle_lines,
        )
        if sleep_cycle_match is not None:
            result[guard_id] += collections.Counter(
                range(int(sleep_cycle_match.group("minute_asleep")), int(sleep_cycle_match.group("minute_awake")))
            )

            i += 2
        else:
            i += 1

    return dict(result)


def test_sleep_schedules_from_strings():
    assert guard_sleep_schedules_from_strings(EXAMPLE_INPUT.splitlines()) == {
        10: collections.Counter(
            {
                5: 1,
                6: 1,
                7: 1,
                8: 1,
                9: 1,
                10: 1,
                11: 1,
                12: 1,
                13: 1,
                14: 1,
                15: 1,
                16: 1,
                17: 1,
                18: 1,
                19: 1,
                20: 1,
                21: 1,
                22: 1,
                23: 1,
                24: 2,
                25: 1,
                26: 1,
                27: 1,
                28: 1,
                30: 1,
                31: 1,
                32: 1,
                33: 1,
                34: 1,
                35: 1,
                36: 1,
                37: 1,
                38: 1,
                39: 1,
                40: 1,
                41: 1,
                42: 1,
                43: 1,
                44: 1,
                45: 1,
                46: 1,
                47: 1,
                48: 1,
                49: 1,
                50: 1,
                51: 1,
                52: 1,
                53: 1,
                54: 1,
            }
        ),
        99: collections.Counter(
            {
                36: 1,
                37: 1,
                38: 1,
                39: 1,
                40: 2,
                41: 2,
                42: 2,
                43: 2,
                44: 2,
                45: 3,
                46: 2,
                47: 2,
                48: 2,
                49: 2,
                50: 1,
                51: 1,
                52: 1,
                53: 1,
                54: 1,
            }
        ),
    }


def get_part1_answer(lines: typing.List[str]) -> typing.Tuple[int, int]:
    """https://adventofcode.com/2018/day/4"""
    guard_sleep_schedules = guard_sleep_schedules_from_strings(lines)
    guard_asleep_most_minutes_id, minutes_asleep = max(
        guard_sleep_schedules.items(), key=lambda item: sum(item[1].values())
    )
    minute_guard_slept_the_most, _ = minutes_asleep.most_common(1)[0]
    return guard_asleep_most_minutes_id, minute_guard_slept_the_most


def test_part1_example():
    guard_asleep_most_minutes_id, minute_guard_slept_the_most = get_part1_answer(EXAMPLE_INPUT.splitlines())

    assert guard_asleep_most_minutes_id == 10
    assert minute_guard_slept_the_most == 24
    assert guard_asleep_most_minutes_id * minute_guard_slept_the_most == 240


@pytest.fixture
def input_file_lines():
    module_dir = os.path.dirname(os.path.realpath(__file__))
    with pathlib.Path(module_dir, "input.txt").open() as f:
        yield f.read().splitlines()


def test_part1_answer(input_file_lines):
    guard_asleep_most_minutes_id, minute_guard_slept_the_most = get_part1_answer(input_file_lines)

    assert guard_asleep_most_minutes_id == 971
    assert minute_guard_slept_the_most == 38
    assert guard_asleep_most_minutes_id * minute_guard_slept_the_most == 36898


def get_part_2_answer(lines: typing.List[str]) -> typing.Tuple[int, int]:
    """https://adventofcode.com/2018/day/4#part2"""
    guard_sleep_schedules = guard_sleep_schedules_from_strings(lines)
    guard_most_frequently_asleep_on_same_minute_id, minutes_asleep = max(
        guard_sleep_schedules.items(), key=lambda item: max(item[1].values())
    )
    minute_guard_slept_most_frequently, _ = minutes_asleep.most_common(1)[0]

    return guard_most_frequently_asleep_on_same_minute_id, minute_guard_slept_most_frequently


def test_part2_example():
    guard_most_frequently_asleep_on_same_minute_id, minute_guard_slept_most_frequently = get_part_2_answer(
        EXAMPLE_INPUT.splitlines()
    )

    assert guard_most_frequently_asleep_on_same_minute_id == 99
    assert minute_guard_slept_most_frequently == 45
    assert (guard_most_frequently_asleep_on_same_minute_id * minute_guard_slept_most_frequently) == 4455


def test_part2_answer(input_file_lines):
    guard_most_frequently_asleep_on_same_minute_id, minute_guard_slept_most_frequently = get_part_2_answer(
        input_file_lines
    )

    assert guard_most_frequently_asleep_on_same_minute_id == 1877
    assert minute_guard_slept_most_frequently == 43
    assert (guard_most_frequently_asleep_on_same_minute_id * minute_guard_slept_most_frequently) == 80711
