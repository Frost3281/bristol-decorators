import time
from functools import wraps
from typing import Callable, Type, TypeVar, Union

from typing_extensions import ParamSpec

P_Spec = ParamSpec("P_Spec")
T_Ret = TypeVar("T_Ret")


def raise_exc(exc: Exception) -> None:
    raise exc


def retry(
    exception_to_catch: Union[Type[Exception], tuple[Type[Exception], ...]],
    tries: int = 10,
    delay: int = 60 * 10,
    backoff: int = 2,
    callback: Callable[[Exception], None] = lambda exc: None,
    final_err_callback: Callable[[Exception], None] = raise_exc,
) -> Callable[[Callable[P_Spec, T_Ret]], Callable[P_Spec, T_Ret]]:
    """Декоратор для перезапуска функции в случае ошибки."""
    def deco_retry(func: Callable[P_Spec, T_Ret]) -> Callable[P_Spec, T_Ret]:
        @wraps(func)
        def f_retry(*args: P_Spec.args, **kwargs: P_Spec.kwargs) -> T_Ret:
            max_tries, max_delay = tries, delay
            while True:
                # noinspection PyBroadException
                try:
                    return func(*args, **kwargs)
                except exception_to_catch as exc:
                    callback(exc)
                    time.sleep(max_delay)
                    max_tries -= 1
                    max_delay *= backoff
                    if max_tries < 1:
                        final_err_callback(exc)
        return f_retry
    return deco_retry
