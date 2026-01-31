import schedule_parser as sp
from config import *


from config import URL, DAYS_OF_WEEK_START_MARKER, DAYS_OF_WEEK_STOP_MARKER, CLASSES_START_MARKER, CLASSES_STOP_MARKER
    
config = {
    'DAYS_START': DAYS_OF_WEEK_START_MARKER,
    'DAYS_STOP': DAYS_OF_WEEK_STOP_MARKER,
    'CLASSES_START': CLASSES_START_MARKER,
    'CLASSES_STOP': CLASSES_STOP_MARKER
}

parser = sp.ScheduleParser(URL, config)

data = parser.fetch_data().parse()
sp.save_json(data)