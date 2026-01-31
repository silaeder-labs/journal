from dotenv import load_dotenv
from os import getenv

load_dotenv()

#table url setting
URL = getenv("URL", 
    "https://docs.google.com/spreadsheets/d/"
    "1sIB6LEA4Zsw-O5EblznpNE778TByRzBMoVrH8OPLnoE/export"
    "?format=csv&gid=1302435266"
)