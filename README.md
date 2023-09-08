# **bristol-decorators**

Вспомогательные декораторы Бристоль.

**bristol-log-decorator**: работает с асинхронными/синхронными функциями,
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