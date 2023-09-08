import inspect
import time
from functools import wraps
from typing import (
    Awaitable,
    Callable,
    TypeVar,
    Union,
    cast,
    overload,
)
from typing_extensions import ParamSpec

from .protocols import Logger
from .services import get_default_logger, get_signature_repr

P_Spec = ParamSpec("P_Spec")
T_Ret = TypeVar("T_Ret")


def log(
    logger_instance: Union[Logger, None] = None
) -> Callable[[Callable[P_Spec, T_Ret]], Callable[P_Spec, T_Ret]]:
    _logger: Logger = logger_instance or get_default_logger()  # type: ignore

    @overload
    def decorator(
        func: Callable[P_Spec, T_Ret],
    ) -> Callable[P_Spec, T_Ret]:
        ...

    @overload
    def decorator(  # type: ignore
        func: Callable[P_Spec, Awaitable[T_Ret]],
    ) -> Callable[P_Spec, Awaitable[T_Ret]]:
        ...

    def decorator(
        func: Union[Callable[P_Spec, T_Ret], Callable[P_Spec, Awaitable[T_Ret]]],
    ) -> Callable[P_Spec, T_Ret]:
        is_async_function = inspect.iscoroutinefunction(func)
        time_start = time.perf_counter()

        @wraps(func)
        async def async_wrapper(
            *args: P_Spec.args,
            **kwargs: P_Spec.kwargs,
        ) -> T_Ret:
            signature = get_signature_repr(*args, **kwargs)
            _logger.debug(
                f"function '{func.__name__}' called with args {signature}",
            )
            try:
                result = await cast(Awaitable[T_Ret], func(*args, **kwargs))
                _logger.debug(
                    f"function '{func.__name__}' ended job with args {signature}, "
                    + f"work_time = {time.perf_counter() - time_start}",
                )
                return result
            except Exception as exc:
                _log_exception_with_raise(
                    _logger,
                    func.__name__,
                    exc,
                    signature,
                )

        @wraps(func)
        def wrapper(
            *args: P_Spec.args,
            **kwargs: P_Spec.kwargs,
        ) -> T_Ret:
            signature = get_signature_repr(*args, **kwargs)
            _logger.debug(
                f"function '{func.__name__}' called with args {signature}",
            )
            try:
                result = cast(T_Ret, func(*args, **kwargs))
                _logger.debug(
                    f"function '{func.__name__}' ended job with args {signature}, "
                    + f"work_time = {time.perf_counter() - time_start}",
                )
                return result
            except Exception as exc:
                _log_exception_with_raise(
                    _logger,
                    func.__name__,
                    exc,
                    signature,
                )

        return (
            cast(Callable[P_Spec, T_Ret], async_wrapper)
            if is_async_function
            else wrapper
        )

    return decorator


def _log_exception_with_raise(
    logger: Logger,
    func_name: str,
    exc: Exception,
    signature: str,
):
    logger.exception(
        f"Exception raised in '{func_name}'. "
        + f"Description: {repr(exc)}"
        + f"Function args: {signature}",
    )
    raise exc
