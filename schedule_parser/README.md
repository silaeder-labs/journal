# Парсер расписания
> программа которая позволяет парсить расписание силаэдра из google таблицы

---

<h2 id="possibilities">Возможности</h2>

в парсере есть функция `init_structured_table()` которая возвращает готовую таблицу расписания

<h3>Как получить нужную информацию?</h3>

1. укажите день недели (0-5)
2. укажите класс (0-7)
4. укажите номер урока (0-11)
3. укажите подкласс (0-1) 

> [!NOTE]
> ```python
> strucutred_table = init_structured_table(url)
> print(strucutred_table[4]) # выведет расписание пятницы
> ```
> ```python
> strucutred_table = init_structured_table()
> print(strucutred_table[0][4]) # выведет расписание 9С в понедельник
> ```
> ```python
> strucutred_table = init_structured_table()
> print(strucutred_table[2][4][3]) # выведет четвертый урок обоих подгрупп 9С в среду
> ```
> ```python
> strucutred_table = init_structured_table()
> print(strucutred_table[3][1][4][0]) # выведет пятый урок первой подгруппы 6С в четверг
> ```

<h3>Как изменить таблицу и лист с которых библиотека получает информацию?</h3>

источники нужно указать при вызове функции `init_structured_table()`

> [!NOTE]
> ```
> import schedule_parser as sp
> url = (
>     "https://docs.google.com/spreadsheets/d/" # гугл таблицы
>     "1W9qMX1QzlZvBkNS0lwA7ZKyMGUlR9dBZnAE9JwqHRHg/export" # id таблицы
>     "?format=csv&gid=917584427" # id страницы
> )
> 
> strucutred_table = sp.init_structured_table(url=url)
> ```

<h3>Как использовать кастомные классы и дни недели</h3>

классы и дни недели можно передать в функцию `init_structured_table()`

> [!NOTE]
> ```
> import schedule_parser as sp
> url = (
>     "https://docs.google.com/spreadsheets/d/" # гугл таблицы
>     "1W9qMX1QzlZvBkNS0lwA7ZKyMGUlR9dBZnAE9JwqHRHg/export" # id таблицы
>     "?format=csv&gid=917584427" # id страницы
> )
> days_of_week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
> classes = ["5С", "6С", "7С", "8С", "9С", "10С", "10Т", "11С"]
> 
> strucutred_table = sp.init_structured_table(url=url, days_of_week=days_of_week, classes=classes)
> ```

