# Парсер расписания
> программа которая позволяет парсить расписание силаэдра из google таблицы

---

<h2 id="possibilities">Как получить данные</h2>

1. Настройте пермеменные
> [!NOTE]
> В файле config.py
> ```python
> url = (
>     "https://docs.google.com/spreadsheets/d/" # гугл таблицы
>     "1W9qMX1QzlZvBkNS0lwA7ZKyMGUlR9dBZnAE9JwqHRHg/export" # id таблицы
>     "?format=csv&gid=917584427" # id страницы
> )
> 
> classes_start_marker = "5С" #маркер первого класса в таблице
> classes_stop_marker = "Питание в столовой" #маркер после последнего класса в таблице
> days_of_week_start_marker = "Понедельник" #маркер первого дня
> days_of_week_stop_marker = "Суббота" #маркер последнего дня
> ```

2. Импортируйте библиотеку и данные из конфига
> [!NOTE]
> в вашем файле
> ```python
> import schedule_parser as sp
> from config import *
> 
> 
> table = sp.init_table(url)
> days_of_week = sp.get_days_of_week(table, days_of_week_start_marker, days_of_week_stop_marker)
> classes = sp.get_classes(table, classes_start_marker, classes_stop_marker)
> lessons = sp.get_lessons_of_day(table,days_of_week[1],classes[1])
> 
> sp.convert_to_json(sp.init_dictionary(days_of_week, classes, lessons))
> ```

на выходе будет .json файл с расписанием из указаной таблицы
