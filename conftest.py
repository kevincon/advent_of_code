import pathlib
import typing

import _pytest.fixtures
import pytest

InputFileParser = typing.Callable[[str], typing.List[str]]


@pytest.fixture(scope="function")
def input_file_parser(request: _pytest.fixtures.FixtureRequest) -> InputFileParser:
    def _parse(input_file_name: str) -> typing.List[str]:
        test_function = request.function
        file_containing_test_function = pathlib.Path(test_function.__code__.co_filename)
        folder_containing_test_file = file_containing_test_function.parent
        input_file = folder_containing_test_file / input_file_name
        with input_file.open() as f:
            return f.read().splitlines()

    return _parse
