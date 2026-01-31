import requests
import csv
import io
import json
import re
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple

@dataclass
class LessonGroup:
    name: str
    cabinet: str
    groups: List[int]

@dataclass
class TimeSlot:
    start: str
    end: str
    lessons: List[LessonGroup] = field(default_factory=list)

class ScheduleParser:
    CABINET_PATTERNS = [
        r'\s+(\d{1,3}[а-яА-Я]?)$',
        r'\s+([А-Яа-я]{1,3}\d{1,3})$',
        r'\s+(спорт\.?\s*зал|актовый\s*зал|библиотека)$',
    ]

    def __init__(self, url: str, config: dict):
        self.url = url
        self.cfg = config
        self.table: List[List[str]] = []

    def fetch_data(self):
        response = requests.get(self.url)
        response.raise_for_status()
        text = response.content.decode("utf-8")
        self.table = list(csv.reader(io.StringIO(text)))
        return self

    def _extract_lesson_info(self, text: str) -> Tuple[str, str]:
        text = text.strip()
        if not text:
            return "", ""
        
        for pattern in self.CABINET_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return text[:match.start()].strip(), match.group(1).strip()
        return text, ""

    def _find_markers(self) -> Tuple[Dict[str, int], Dict[str, int]]:
        days = {}
        classes = {}
        
        is_reading_days = False
        for i, row in enumerate(self.table):
            val = row[0].strip().lower()
            if val == self.cfg['DAYS_START'].lower():
                is_reading_days = True
            if is_reading_days and row[0]:
                days[row[0]] = i
                if val == self.cfg['DAYS_STOP'].lower():
                    break
        
        is_reading_classes = False
        for j, val in enumerate(self.table[0]):
            val_clean = val.strip().lower()
            if val_clean == self.cfg['CLASSES_START'].lower():
                is_reading_classes = True
            if is_reading_classes and val:
                classes[val] = j
                if val_clean == self.cfg['CLASSES_STOP'].lower():
                    break
                    
        return days, classes

    def parse(self) -> Dict:
        day_markers, class_markers = self._find_markers()
        day_names = list(day_markers.keys())
        class_names = list(class_markers.keys())
        class_indices = list(class_markers.values())
        
        schedule = {}

        for i, day_name in enumerate(day_names):
            day_start_row = day_markers[day_name]
            # Определяем, где заканчивается текущий день
            next_day_row = day_markers[day_names[i+1]] if i+1 < len(day_names) else len(self.table)
            
            day_data = {}

            for j, class_name in enumerate(class_names):
                class_start_col = class_indices[j]
                # Определяем границы колонок для групп одного класса
                next_class_col = class_indices[j+1] if j+1 < len(class_indices) else len(self.table[0])
                
                lessons_in_day = {}

                # Идем по строкам уроков внутри дня
                for row_idx in range(day_start_row, next_day_row):
                    row = self.table[row_idx]
                    lesson_num = row[1]
                    if not lesson_num: continue # Пропускаем пустые строки

                    slot = TimeSlot(start=row[2], end=row[3])
                    
                    # Группировка подгрупп (физика/англ) в один объект
                    lesson_groups_map = {}
                    
                    for col_idx in range(class_start_col, next_class_col):
                        raw_text = row[col_idx]
                        name, cab = self._extract_lesson_info(raw_text)
                        
                        if not name: continue
                        
                        key = f"{name}||{cab}"
                        if key not in lesson_groups_map:
                            lesson_groups_map[key] = LessonGroup(name, cab, [])
                        
                        # Номер подгруппы — это смещение от начала колонки класса
                        lesson_groups_map[key].groups.append(col_idx - class_start_col + 1)

                    slot.lessons = list(lesson_groups_map.values())
                    if slot.lessons:
                        lessons_in_day[lesson_num] = asdict(slot)

                day_data[class_name] = lessons_in_day
            
            schedule[day_name] = day_data
            
        return schedule

def save_json(data: dict, filename: str = "data/data.json"):
    path = Path.cwd() / Path(filename)
    path.parent.mkdir(exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Сохранено в {path}")

if __name__ == "__main__":
    from config import URL, DAYS_OF_WEEK_START_MARKER, DAYS_OF_WEEK_STOP_MARKER, CLASSES_START_MARKER, CLASSES_STOP_MARKER
    
    config = {
        'DAYS_START': DAYS_OF_WEEK_START_MARKER,
        'DAYS_STOP': DAYS_OF_WEEK_STOP_MARKER,
        'CLASSES_START': CLASSES_START_MARKER,
        'CLASSES_STOP': CLASSES_STOP_MARKER
    }

    parser = ScheduleParser(URL, config)
    
    data = parser.fetch_data().parse()
    save_json(data)