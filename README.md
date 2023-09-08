# **bristol-decorators**

Вспомогательные декораторы Бристоль.
<br><br><br>
**log**: работает с асинхронными/синхронными функциями,
логирует в дебаге начало/завершение выполнения функции с переданными аргументами и временем работы функции. Логирует исключения.
Сохраняет исходную типизацию.

Применение:

```python
from bristol_log_decorator import log

@log()
def check_function(check_list: list[str]) -> None:
    print(check_list)

check_function(check_list=[1, 2, 3])
```

```
function 'check_function' called with args check_list=[1, 2, 3]
function 'check_function' ended job with args check_list=[1, 2, 3], work_time = 0.003176100000000015
```

Аналогично работает с асинхронными функциями:

```python
import asyncio
from bristol_log_decorator import log

@log()
async def check_function(check_list: list[str]) -> None:
    print(check_list)

asyncio.run(check_function(check_list=[1, 2, 3]))
```

В декоратор можно передавать также instance других logging-библиотек,
кроме стандартной библиотеки **logging**, например, **loguru**.

```python
import loguru
from bristol_log_decorator import log

@log(logger_instance=loguru.logger)
def check_function(check_list: list[str]) -> None:
    print(check_list)
```
<br><br><br>
**retry**: Декоратор для перезапуска функции в случае заданных ошибок. Помимо количества попыток, задержки между ними и backoff'а принимает также возможные callback'и на ошибки, после которых ещё остаются tries, и на финальную ошибку.
Работает с синхронными функциями. Сохраняет исходную типизацию.

Применение:

```python
from retry_decorator import retry


@retry(
    ValueError,
    tries=3,
    delay=10,
    backoff=2,
    callback=lambda exc: None,  # остались tries, ничего не делаем
    final_err_callback=func_with_logic_to_reraise_exception_example,
)
def my_function() -> str:
    raise ValueError("Error")
```
