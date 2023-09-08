from typing import Any

import pytest


class MockLogger:
    """Заглушка для логгера."""

    def __init__(self) -> None:
        self.logged_messages: list[str] = []

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logged_messages.append(msg)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.logged_messages.append(msg)


@pytest.fixture()
def mock_logger() -> MockLogger:
    return MockLogger()
