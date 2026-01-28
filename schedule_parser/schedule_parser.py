import requests
import csv
import io
import json
import re
from pathlib import Path
from config import *

def extract_lesson_and_cabinet(lesson_text):
    """
    Извлекает название урока и номер кабинета из текста
    """
    lesson_text = lesson_text.strip()
    if not lesson_text:
        return "", ""
    
    # Паттерны для поиска кабинетов
    cabinet_patterns = [
        r'\s+(\d{1,3}[а-яА-Я]?)$',  # номер кабинета в конце (123, 45а)
        r'\s+([А-Яа-я]{1,3}\d{1,3})$',  # кабинет типа Ф12, С23
        r'\s+(спорт\.?\s*зал|актовый\s*зал|библиотека)$',  # специальные помещения
    ]
    
    lesson_name = lesson_text
    cabinet = ""
    
    for pattern in cabinet_patterns:
        match = re.search(pattern, lesson_text, re.IGNORECASE)
        if match:
            cabinet = match.group(1).strip()
            lesson_name = lesson_text[:match.start()].strip()
            break
    
    return lesson_name, cabinet

def init_table(url):
    response = requests.get(url)
    response.raise_for_status()

    text = response.content.decode("utf-8")
    reader = csv.reader(io.StringIO(text))
    table = []

    for row in reader:
        table.append(row)

    return table

def get_days_of_week(table, days_of_week_start_marker, days_of_week_stop_marker):
    days_of_week = []
    days_of_week_indexes = []

    isReading = False

    for i in range(len(table)):
        word = table[i][0]
        if not isReading:
            if(word.lower() == days_of_week_start_marker.lower()):
                days_of_week.append(word)
                days_of_week_indexes.append(i)
                isReading = True
        else:
            if(word != ''):
                days_of_week.append(word)
                days_of_week_indexes.append(i)
                if(word.lower() == days_of_week_stop_marker.lower()):
                    break

    return days_of_week, days_of_week_indexes

def get_classes(table, classes_start_marker, classes_stop_marker):
    classes = []
    classes_indexes = []

    isReading = False

    for i in range(len(table[0])):
        word = table[0][i]
        if not isReading:
            if(word.lower() == classes_start_marker.lower()):
                classes.append(word)
                classes_indexes.append(i)
                isReading = True
        else:
            if(word != ''):
                classes_indexes.append(i)
                if(word.lower() == classes_stop_marker.lower()):
                    break
                classes.append(word)

    return classes, classes_indexes

def get_lessons_of_day(table, day_of_week_indexes, classes_indexes):
    lessons = []
    lessons_start_time = []
    lessons_end_time = []
    lessons_indexes = []

    for i in range(len(day_of_week_indexes)):
        lessons_start_time.append([])
        lessons_end_time.append([])
        lessons_indexes.append([])
        lessons.append([])

        for j in range(day_of_week_indexes[i], len(table)):
            index = table[j][1]
            start_time = table[j][2]
            end_time = table[j][3]

            if(index == ""):
                break

            lessons_indexes[i].append(int(index))
            lessons_start_time[i].append(start_time)
            lessons_end_time[i].append(end_time)

        for j in range(len(classes_indexes)-1):
            lessons[i].append([])
            for v in range(len(lessons_indexes[i])):
                groups = []
                lesson_row = day_of_week_indexes[i] + v + 1
                for u in range(classes_indexes[j], classes_indexes[j+1]):
                    groups.append(table[lesson_row][u])

                lessons[i][j].append(groups)

    return lessons, lessons_start_time, lessons_end_time, lessons_indexes

def convert_to_json(table):
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent

    final_path = script_dir / "data/data.json"
    
    # Создаем папку data если её нет
    final_path.parent.mkdir(exist_ok=True)
    
    with open(final_path, 'w', encoding='utf-8') as f:
        json.dump(table, f, ensure_ascii=False, indent=2)
    
    print(f"Данные сохранены в: {final_path}")

def debug_lessons_structure(lessons, day_index=0, class_index=0):
    """
    Функция для отладки структуры уроков
    """
    print(f"Отладка структуры уроков для дня {day_index}, класса {class_index}:")
    
    if day_index < len(lessons[0]) and class_index < len(lessons[0][day_index]):
        day_lessons = lessons[0][day_index][class_index]
        
        for lesson_index, lesson_time in enumerate(day_lessons):
            print(f"  Урок {lesson_index + 1}:")
            for group_index, group_lesson in enumerate(lesson_time):
                print(f"    Группа {group_index + 1}: '{group_lesson}'")
    else:
        print("  Индексы выходят за границы данных")

def init_dictionary(days_of_week, classes, lessons):
    dict = {}
    
    for x1 in range(len(days_of_week[0])):  # дни недели
        day_dict = {}
        
        for x2 in range(len(classes[0])):  # классы
            class_dict = {}
            
            for x3 in range(len(lessons[3][x1])):  # уроки в дне
                lesson_dict = {}
                lesson_dict["from"] = lessons[1][x1][x3]
                lesson_dict["to"] = lessons[2][x1][x3]

                # Собираем все уроки для данного времени
                all_lessons_for_time = lessons[0][x1][x2][x3]
                
                # Группируем уроки по содержимому
                lesson_groups = {}
                
                for x4 in range(len(all_lessons_for_time)):
                    lesson_text = str(all_lessons_for_time[x4]).strip()
                    
                    if lesson_text == "":
                        continue
                    
                    # Извлекаем название урока и кабинет
                    lesson_name, lesson_cab = extract_lesson_and_cabinet(lesson_text)
                    
                    if lesson_name == "":
                        continue
                    
                    # Создаем ключ для группировки одинаковых уроков
                    lesson_key = f"{lesson_name}_{lesson_cab}"
                    
                    if lesson_key not in lesson_groups:
                        lesson_groups[lesson_key] = {
                            "name": lesson_name,
                            "cabinet": lesson_cab,
                            "groups": []
                        }
                    
                    # Добавляем номер группы (позицию в расписании + 1)
                    lesson_groups[lesson_key]["groups"].append(x4 + 1)
                
                # Формируем финальную структуру уроков
                lessons_list = []
                for lesson_info in lesson_groups.values():
                    lesson_data = {
                        "name": lesson_info["name"],
                        "cabinet": lesson_info["cabinet"],
                        "groups": lesson_info["groups"]  # список групп, для которых предназначен урок
                    }
                    lessons_list.append(lesson_data)

                lesson_dict["lessons"] = lessons_list
                
                # Добавляем урок только если есть хотя бы один урок
                if lessons_list:
                    class_dict[lessons[3][x1][x3]] = lesson_dict

            day_dict[classes[0][x2]] = class_dict

        dict[days_of_week[0][x1]] = day_dict

    return dict    


def print_schedule_summary(schedule_dict, day="Понедельник", class_name="5С"):
    """
    Выводит краткое расписание для отладки
    """
    print(f"\n=== Расписание {class_name} на {day} ===")
    
    if day in schedule_dict and class_name in schedule_dict[day]:
        day_schedule = schedule_dict[day][class_name]
        
        for lesson_num, lesson_info in day_schedule.items():
            print(f"\n{lesson_num} урок ({lesson_info['from']} - {lesson_info['to']}):")
            
            for lesson in lesson_info['lessons']:
                groups_str = ", ".join(map(str, lesson['groups']))
                cabinet_str = f" (каб. {lesson['cabinet']})" if lesson['cabinet'] else ""
                print(f"  • {lesson['name']}{cabinet_str} - группы: {groups_str}")
    else:
        print("Данные не найдены")

if __name__ == "__main__":
    print("собираем информаци...")
    table = init_table(URL)
    
    days_of_week = get_days_of_week(table, DAYS_OF_WEEK_START_MARKER, DAYS_OF_WEEK_STOP_MARKER)
    
    classes = get_classes(table, CLASSES_START_MARKER, CLASSES_STOP_MARKER)
    
    lessons = get_lessons_of_day(table, days_of_week[1], classes[1])
    
    # debug_lessons_structure(lessons, 0, 0)
    
    schedule_dict = init_dictionary(days_of_week, classes, lessons)
    
    convert_to_json(schedule_dict)
    
    print("Готово!")