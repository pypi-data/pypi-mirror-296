# PIUnit

Добавляет возможность тестировать код с функциями print и input
<br>

Установите библиотеку:
```
pip install piunit
```

<br>

Пример использования:
```
from main import print_hello_world, log_user_state, get_data
from piunit.test import BasePIUnitTest


class TestOne(BasePIUnitTest):
    def test_one(self):
        self.assertPrint(print_hello_world, ['Hello, World!'])
        self.assertInput(log_user_state, ['Смена пароля', 'Пароль успешно изменён'], True, 'new_pass')
        self.assertPrintInput(get_data, [10, 3, 2], ['Результат выполнения кода: 15'])
```

Описание методов класса BasePIUnitTest:
<pre>
+ assertPrint(test_func: Callable, prints: SupportsIndex,
                   all_: bool = False)
  Тестирует код с функцией print.
    Проверяет, напечаталось ли в print то, что ожидалось.
    Args:
      test_func: Callable (тестируемый объект)
      prints: SupportsIndex (значения для print)
      all_: bool (при True - вернёт ошибку если остались неиспользованные
        значения)
      *args, **kwargs: аргументы для тестируемой функции


+ assertInput(test_func: Callable, inputs: SupportsIndex,
                   all_: bool = False)

  Тестирует код с функцией input.
  Возвращает указанные данные при вызове input.

  Args:
    test_func: Callable (тестируемый объект)
    inputs: SupportsIndex (значения для input)
    all_: bool (при True, вернёт ошибку если остались неиспользованные
    значения)
    *args, **kwargs: аргументы для тестируемой функции


+ assertPrintInput(self, test_func: Callable,
                         inputs: SupportsIndex,
                         prints: SupportsIndex,
                         all_: bool = False
                         ):

  Тестирует код с функцией print и input.

  Подставляет по порядку данные из prints и inputs.

  Args:
    test_func: Callable (тестируемый объект)
    inputs: SupportsIndex (значения для input)
    prints: SupportsIndex (значения для print)
    all_: bool (при True, вернёт ошибку если остались неиспользованные
    значения)
    *args, **kwargs: аргументы для тестируемой функции
</pre>
