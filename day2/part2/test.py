import collections
import itertools
import operator
import os
import pathlib
import typing


def find_id_pair_that_differs_by_one_character(ids: typing.Iterable[str]) -> typing.Optional[typing.Tuple[str, str]]:
    combinations: typing.List[typing.Tuple[str, str]] = itertools.combinations(ids, 2)
    for combination in combinations:
        letter_pairs = zip(*combination)
        diff_checks = itertools.starmap(operator.ne, letter_pairs)
        diff_counter = collections.Counter(diff_checks)
        if diff_counter[True] == 1:
            return combination
    return None


def test_find_id_pair_that_differs_by_one_character():
    assert find_id_pair_that_differs_by_one_character([
        'abcde',
        'fghij',
        'klmno',
        'pqrst',
        'fguij',
        'axcye',
        'wvxyz',
    ]) == ('fghij', 'fguij')


def get_answer(ids: typing.Iterable[str]) -> str:
    """https://adventofcode.com/2018/day/2#part2"""
    answer_pair = find_id_pair_that_differs_by_one_character(ids)
    if not answer_pair:
        raise Exception('No id pair that differs by only one character')

    letter_pairs = zip(*answer_pair)
    common_letter_pairs = filter(lambda pair: operator.eq(*pair), letter_pairs)
    return ''.join(list(zip(*common_letter_pairs))[0])


def test_example():
    assert get_answer([
        'abcde',
        'fghij',
        'klmno',
        'pqrst',
        'fguij',
        'axcye',
        'wvxyz',
    ]) == 'fgij'


def test_answer():
    module_dir = os.path.dirname(os.path.realpath(__file__))
    with pathlib.Path(module_dir, 'input.txt').open() as f:
        assert get_answer(f.read().splitlines()) == 'cvgywxqubnuaefmsljdrpfzyi'
