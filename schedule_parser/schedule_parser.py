import requests
import csv
import io
import json
from config import *

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
                classes.append(word)
                classes_indexes.append(i)
                if(word.lower() == classes_stop_marker.lower()):
                    break

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

        for j in range(len(classes_indexes)):
            lessons[i].append([])
            for v in range(len(lessons_indexes[i])):
                groups = []
                lesson_row = day_of_week_indexes[i] + v + 1

                if(j < len(classes_indexes)-1):
                    for u in range(classes_indexes[j], classes_indexes[j+1]):
                        if u < len(table[lesson_row]):
                            groups.append(table[lesson_row][u])
                else:
                    for u in range(classes_indexes[j], classes_indexes[j]+2):
                        groups.append(table[lesson_row][u])

                lessons[i][j].append(groups)

    return lessons, lessons_start_time, lessons_end_time, lessons_indexes

def convert_to_json(table):
    file_name = "data.json"
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(table, f, ensure_ascii=False, indent=2)

def init_dictionary(days_of_week, classes, lessons):
    dict = {}
    for x1 in range(len(days_of_week[0])):
        day_dict = {}
        for x2 in range(len(classes[0])):
            class_dict = {}
            for x3 in range(len(lessons[3][x1])):
                lesson_dict = {}
                lesson_dict["from"] = lessons[1][x1][x3]
                lesson_dict["to"] = lessons[2][x1][x3]

                lesson = {}

                for x4 in range(len(lessons[0][x1][x2][x3])):
                    group = {}

                    lesson_name = str(lessons[0][x1][x2][x3][x4])
                    lesson_cab = lesson_name[len(lesson_name)-3:]
                    lesson_name = lesson_name[:len(lesson_name)-3]

                    group["name"] = lesson_name
                    group["cab"] = lesson_cab

                    lesson["group" + str(x4+1)] = group

                lesson_dict["lesson"] = lesson

                class_dict[lessons[3][x1][x3]] = lesson_dict

            day_dict[classes[0][x2]] = class_dict

        dict[days_of_week[0][x1]] = day_dict

    return dict
    


if __name__ == "__main__":
    # data_list = [
    #     {"monday": {"9C": {"1": {"from": "1678886400", "to":"1678886400"}, "lesson": {"group1": {"name": "sleep", "cab":209}}}}},
    # ]
    # convert_to_json(init_dictionary(days_of_week,classes))
    table = init_table(url)
    days_of_week = get_days_of_week(table, days_of_week_start_marker, days_of_week_stop_marker)
    classes = get_classes(table, classes_start_marker, classes_stop_marker)
    lessons = get_lessons_of_day(table,days_of_week[1],classes[1])

    convert_to_json(init_dictionary(days_of_week, classes, lessons))