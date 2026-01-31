# Парсер расписания
> программа которая позволяет парсить расписание силаэдра из google таблицы

---

<h2 id="possibilities">Как получить данные</h2>

1. Настройте пермеменные в `.env`
пример конфига
```
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

---

## Исправленные проблемы (январь 2026)

### 1. Проблема с автоматической группировкой
**Было**: Когда у первой группы есть урок, парсер автоматически определял все уроки в одну группу.
**Стало**: Парсер теперь правильно группирует уроки по их содержимому, а не по позиции в таблице.

### 2. Проблема с уроками на несколько групп
**Было**: Когда один урок предназначен для двух групп, он отображался только у первой группы.
**Стало**: Уроки теперь корректно отображаются для всех групп с указанием номеров групп.

## Новая структура данных

```json
{
  "день_недели": {
    "класс": {
      "номер_урока": {
        "from": "время_начала",
        "to": "время_окончания",
        "lessons": [
          {
            "name": "название_урока",
            "cabinet": "номер_кабинета",
            "groups": [1, 2]
          }
        ]
      }
    }
  }
}
```

## Улучшения

- Улучшенное извлечение номеров кабинетов с поддержкой различных форматов
- Отладочная информация для диагностики проблем
- Красивый вывод расписания для проверки результатов
- Автоматическое создание папки для данных

## Быстрый запуск

```bash
python schedule_parser.py
```

Результат сохраняется в `data/data.json`.