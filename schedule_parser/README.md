# Парсер расписания
> программа которая позволяет парсить расписание силаэдра из google таблицы

---

<h2 id="possibilities">Как получить данные</h2>

1. Настройте пермеменные в `.env`
пример конфига
```python
#  гугл таблицы, id таблицы, id страницы
URL = https://docs.google.com/spreadsheets/d/1W9qMX1QzlZvBkNS0lwA7ZKyMGUlR9dBZnAE9JwqHRHg/export?format=csv&gid=917584427

#маркеры
CLASSES_START_MARKER = 5С
CLASSES_STOP_MARKER = Питание в столовой
DAYS_OF_WEEK_START_MARKER = Понедельник
DAYS_OF_WEEK_STOP_MARKER = Суббота
```

2. Импортируйте библиотеку и данные из конфига
```python
import schedule_parser as sp
from config import *

table = sp.init_table(url)
days_of_week = sp.get_days_of_week(table, days_of_week_start_marker, days_of_week_stop_marker)
classes = sp.get_classes(table, classes_start_marker, classes_stop_marker)
lessons = sp.get_lessons_of_day(table,days_of_week[1],classes[1])

sp.convert_to_json(sp.init_dictionary(days_of_week, classes, lessons))
```

на выходе будет `.json` файл с расписанием из указаной таблицы
