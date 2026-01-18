import requests
import csv
import io

days_of_week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
classes = ["5С", "6С", "7С", "8С", "9С", "10С", "10Т", "11С"]

def init_table(url):
    response = requests.get(url)
    response.raise_for_status()

    text = response.content.decode("utf-8")

    reader = csv.reader(io.StringIO(text))

    table = []

    for row in reader:
        table.append(row)

    return table


def get_days_of_week_indexes(table, days_of_week):
    days_of_week_indexes = [0,0,0,0,0,0]

    for i in range(len(table)):
        word = table[i][0]
        for j in range(len(days_of_week)):
            if days_of_week[j].lower() in word.lower():
                days_of_week_indexes[j] = i

    return days_of_week_indexes

def get_classes_indexes(table, classes):
    classes_indexes = [0,0,0,0,0,0,0,0]

    for i in range(len(table[0])):
        word = table[0][i]
        for j in range(len(classes)):
            if classes[j].lower() in word.lower():
                classes_indexes[j] = i

    return classes_indexes

def init_structured_table(url, days_of_week=days_of_week, classes=classes): # можно ставить кастомные дни недели и классы
    table = init_table(url=url)
    days_of_week_indexes = get_days_of_week_indexes(table, days_of_week)
    classes_indexes = get_classes_indexes(table, classes)
    strucutred_table = []

    for i in range(len(days_of_week_indexes)-1):
        strucutred_table.append([])
        for j in range(len(classes_indexes)-1):
            strucutred_table[i].append([])
            for row in table[days_of_week_indexes[i]:days_of_week_indexes[i+1]]:
                strucutred_table[i][j].append(row[classes_indexes[j]:classes_indexes[j+1]])

    return strucutred_table

if __name__ == "__main__":
    print(init_table())