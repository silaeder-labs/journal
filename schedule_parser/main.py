import requests
import csv
import io

url = (
    "https://docs.google.com/spreadsheets/d/"
    "1W9qMX1QzlZvBkNS0lwA7ZKyMGUlR9dBZnAE9JwqHRHg/export"
    "?format=csv&gid=1367877017"
)

def init_table():
    response = requests.get(url)
    response.raise_for_status()

    text = response.content.decode("utf-8")

    reader = csv.reader(io.StringIO(text))

    table = []

    for row in reader:
        table.append(row)

    return table


def get_days_of_week_indexes(table):
    days_of_week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
    days_of_week_indexes = [0,0,0,0,0,0]

    for i in range(len(table)):
        word = table[i][0]
        for j in range(len(days_of_week)):
            if days_of_week[j] in word:
                days_of_week_indexes[j] = i

    return days_of_week_indexes

def get_classes_indexes(table):
    classes = ["5С", "6С", "7С", "8С", "9С", "10С", "10Т", "11С"]
    classes_indexes = [0,0,0,0,0,0,0,0]

    for i in range(len(table[0])):
        word = table[0][i]
        for j in range(len(classes)):
            if classes[j] in word:
                classes_indexes[j] = i

    return classes_indexes

def init_structured_table():
    table = init_table()
    days_of_week_indexes = get_days_of_week_indexes(table)
    classes_indexes = get_classes_indexes(table)
    strucutred_table = []

    for i in range(len(days_of_week_indexes)-1):
        strucutred_table.append([])
        for j in range(len(classes_indexes)-1):
            strucutred_table[i].append([])
            for row in table[days_of_week_indexes[i]:days_of_week_indexes[i+1]]:
                strucutred_table[i][j].append(row[classes_indexes[j]:classes_indexes[j+1]])

    return strucutred_table