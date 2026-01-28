import requests
import csv
import io
import json
from pathlib import Path
from config import URL

def init_table(url):
    response = requests.get(url)
    response.raise_for_status()

    text = response.content.decode("utf-8")
    reader = csv.reader(io.StringIO(text))
    table = []

    for row in reader:
        table.append(row)

    return table

def convert_to_dictionary(table):
    homeworks = {}
    subject = "Предмет"
    date = table[0][1]
    homework = table[0][2]
    for i in range(1,len(table)):
        sub_dict = {}
        sub_dict[subject] = table[i][0]
        sub_dict[date] = table[i][1]
        sub_dict[homework] = table[i][2]

        homeworks[i] = sub_dict

    return homeworks

def save_to_json(dict):
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent

    final_path = script_dir / "data/data.json"
    
    final_path.parent.mkdir(exist_ok=True)
    
    with open(final_path, 'w', encoding='utf-8') as f:
        json.dump(dict, f, ensure_ascii=False, indent=2)
    
    print(f"Данные сохранены в: {final_path}")


# save_to_json(convert_to_dictionary(init_table(URL)))


# print(table)