import schedule_parser as sp
from config import *


table = sp.init_table(url)
days_of_week = sp.get_days_of_week(table, days_of_week_start_marker, days_of_week_stop_marker)
classes = sp.get_classes(table, classes_start_marker, classes_stop_marker)
lessons = sp.get_lessons_of_day(table,days_of_week[1],classes[1])

sp.convert_to_json(sp.init_dictionary(days_of_week, classes, lessons))