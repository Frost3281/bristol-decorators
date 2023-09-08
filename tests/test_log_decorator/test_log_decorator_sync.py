from typing import get_type_hints

import pytest

from bristol_log_decorator.log_decorator import log
from tests.conftest import MockLogger


def sync_func_logging_testing(arg1: int, arg2: str) -> str:
    return f"{arg1} {arg2}"


def test_sync_func_decorator_type_hinting():
    func_annotations = get_type_hints(sync_func_logging_testing)
    deco_annotations = get_type_hints(log()(sync_func_logging_testing))
    assert func_annotations == deco_annotations


def test_sync_function_logs_start_and_end(mock_logger: MockLogger):
    decorated = log(mock_logger)(sync_func_logging_testing)
    result = decorated(10, "abc")
    assert result == "10 abc"
    assert (
        f"function {sync_func_logging_testing.__name__} called with args 10, 'abc'"
        in mock_logger.logged_messages
    )
    assert (
        f"function {sync_func_logging_testing.__name__} ended job with args 10, 'abc'"
        in mock_logger.logged_messages
    )


def test_sync_function_logs_exception(mock_logger: MockLogger):
    decorated = log(mock_logger)(sync_func_logging_testing)
    with pytest.raises(TypeError):
        decorated(10, "", None)  # type: ignore
    assert any(
        [
            msg.startswith(f"Exception raised in {sync_func_logging_testing.__name__}")
            for msg in mock_logger.logged_messages
        ]
    )
    assert any([msg.__contains__("TypeError") for msg in mock_logger.logged_messages])
