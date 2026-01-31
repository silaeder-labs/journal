import requests
import csv
import io
import json
from pathlib import Path

def init_table(url: str) -> list[list[str]]:
    response = requests.get(url)
    response.raise_for_status()

    text = response.content.decode("utf-8")
    reader = csv.reader(io.StringIO(text))
    table = []

    for row in reader:
        table.append(row)

    return table

def convert_to_dictionary(table: list[list[str]]) -> dict[int, dict[str, str]]:
    homeworks: dict[int, dict[str, str]] = {}
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

def save_to_json(data: dict[int, dict[str, str]]) -> None:
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent

    final_path = script_dir / "data/data.json"
    
    final_path.parent.mkdir(exist_ok=True)
    
    with open(final_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Данные сохранены в: {final_path}")
