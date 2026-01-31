import subprocess
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

node_script = os.path.join(
    BASE_DIR,
    "export_marks.js"
)

result = subprocess.check_output(
    ["node", node_script],
    text=True
)

print(result)

# data = json.loads(result)

# print(data)