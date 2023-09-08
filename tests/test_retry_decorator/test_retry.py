import pytest

from retry_decorator.decorator import retry


class RetryTestError(Exception):
    """Ошибка для тестов"""


def test_retry_function_retries_on_exception():
    """Тестируем верное количество retries."""

    tries = 3
    attempts = []

    @retry(Exception, tries=tries, delay=1, backoff=1)
    def my_function() -> str:
        attempts.append(1)
        raise ValueError("Error")

    with pytest.raises(ValueError):
        my_function()
    assert len(attempts) == tries


def test_retry_function_raises_final_error_callback():
    """Тестируем final_error_callback."""

    tries = 3

    @retry(
        Exception,
        tries=tries,
        delay=1,
        backoff=1,
        final_err_callback=_change_exception_type_and_raise,
    )
    def my_function() -> str:
        raise ValueError()

    with pytest.raises(RetryTestError):
        my_function()


def _change_exception_type_and_raise(exception: Exception) -> None:
    raise RetryTestError from exception
