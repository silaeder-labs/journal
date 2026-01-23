from dotenv import load_dotenv
from os import getenv

load_dotenv()

LESSONS_ID = getenv("LESSONS_ID", [33623636, 33623620, 37175860, 33623623, 33623645, 33623617, 33623590, 33623577, 33623648, 33623651, 33623650, 33623605, 33623584, 33623580]).split(",")
LESSONS_NAME = getenv("LESSONS_NAME", ['biology', 'geography', 'english', 'informatics', 'history', 'literature', 'russian', 'chemistry', 'algebra', 'statistics', 'geometry', 'social-science', 'physics', 'pe']).split(",")


for i in range(len(LESSONS_ID)):
    LESSONS_ID[i] = int(LESSONS_ID[i])