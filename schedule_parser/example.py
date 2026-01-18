import main as mn

strucutred_table = mn.init_structured_table()

def print_separator():
    print("="*40)

print(strucutred_table[4]) # выведет расписание пятницы
print_separator()
print(strucutred_table[0][4]) # выведет расписание 9С в понедельник
print_separator()
print(strucutred_table[2][4][3]) # выведет четвертый урок обоих подгрупп 9С в среду
print_separator()
print(strucutred_table[3][1][4][0]) # выведет пятый урок первой подгруппы 6С в четверг
