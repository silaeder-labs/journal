from dotenv import load_dotenv
from os import getenv

load_dotenv()

#table url setting
URL = getenv("URL", 
    "https://docs.google.com/spreadsheets/d/" # гугл таблицы
    "1W9qMX1QzlZvBkNS0lwA7ZKyMGUlR9dBZnAE9JwqHRHg/export" # id таблицы
    "?format=csv&gid=917584427" # id страницы"
)

#markers setting
CLASSES_START_MARKER = getenv("CLASSES_START_MARKER", "5С")
CLASSES_STOP_MARKER = getenv("CLASSES_STOP_MARKER", "Питание в столовой")
DAYS_OF_WEEK_START_MARKER = getenv("DAYS_OF_WEEK_START_MARKER", "Понедельник")
DAYS_OF_WEEK_STOP_MARKER = getenv("DAYS_OF_WEEK_STOP_MARKER", "Суббота")