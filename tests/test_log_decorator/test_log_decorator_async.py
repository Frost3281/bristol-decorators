from typing import get_type_hints

import pytest

from bristol_log_decorator.log_decorator import log
from tests.conftest import MockLogger
from tests.services import check_msg_from_list_contains_text


async def async_func_logging_testing(arg1: int, arg2: str) -> str:
    return f"{arg1} {arg2}"


def test_async_func_decorator_type_hinting():
    func_annotations = get_type_hints(async_func_logging_testing)
    deco_annotations = get_type_hints(log()(async_func_logging_testing))
    assert func_annotations == deco_annotations


@pytest.mark.asyncio
async def test_async_function_logs_start_and_end(mock_logger: MockLogger):
    decorated = log(mock_logger)(async_func_logging_testing)
    result = await decorated(10, "abc")
    assert result == "10 abc"
    assert check_msg_from_list_contains_text(
        f"function '{async_func_logging_testing.__name__}' called with args 10, 'abc'",
        mock_logger.logged_messages,
    )
    assert check_msg_from_list_contains_text(
        f"function '{async_func_logging_testing.__name__}' ended job with args 10, 'abc'",
        mock_logger.logged_messages,
    )


@pytest.mark.asyncio
async def test_async_function_logs_exception(mock_logger: MockLogger):
    decorated = log(mock_logger)(async_func_logging_testing)
    with pytest.raises(Exception):
        await decorated(10, "abc", None)  # type: ignore
    assert check_msg_from_list_contains_text(
        f"Exception raised in '{async_func_logging_testing.__name__}'",
        mock_logger.logged_messages,
    )
    assert check_msg_from_list_contains_text("TypeError", mock_logger.logged_messages)
