import subprocess
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

node_script = os.path.join(
    BASE_DIR,
    "export_subjects.js"
)

result = subprocess.check_output(
    ["node", node_script],
    text=True
)

data = json.loads(result)

print(data["subject_ids"])
print(data["subjects_names"])
