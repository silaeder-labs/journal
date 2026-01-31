import math_table_parser.math_table_parser as mp
from config import *

table = mp.init_table(URL)

dict = mp.convert_to_dictionary(table)

print(dict)