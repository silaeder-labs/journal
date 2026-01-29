from config import *
import info_table_parser as itp

table = itp.init_table(URL)

data = itp.get_columns_indexes(table)

print(itp.convert_to_dictionary(table, data[0], data[1]))
