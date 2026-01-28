from dotenv import load_dotenv
from os import getenv

load_dotenv()

#table url setting
URL = getenv("URL", 
    "https://docs.google.com/spreadsheets/d/"
    "1-l1WqsJtGNtd6Ix5tZesqZeKyGu3zy0dz66r54ecXbE/export"
    "?format=csv&gid=560103071"
)