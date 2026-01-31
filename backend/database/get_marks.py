import subprocess
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_students_marks():
    marks_export = os.path.join(
        BASE_DIR,
        "export_marks.js"
    )

    result = subprocess.check_output(
        ["node", marks_export],
        text=True
    )

    data = json.loads(result)

    students_marks = {}

    for subject in data:
        for date in data[subject]:
            for id in data[subject][date]:
                if id not in students_marks:
                    students_marks[id] = {}

                students_marks[id][subject] = data[subject][date][id]

    return students_marks