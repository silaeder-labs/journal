import schedule_parser as sp
from config import *


table = sp.init_table(URL)
days_of_week = sp.get_days_of_week(table, DAYS_OF_WEEK_START_MARKER, DAYS_OF_WEEK_STOP_MARKER)
classes = sp.get_classes(table, CLASSES_START_MARKER, CLASSES_STOP_MARKER)
lessons = sp.get_lessons_of_day(table,days_of_week[1],classes[1])

sp.convert_to_json(sp.init_dictionary(days_of_week, classes, lessons))