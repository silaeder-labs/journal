import random
import math

def generate_random_marks() -> (list[int], list[int]):
    random_marks = []
    random_middle_marks = []

    for i in range(10):
        random_marks.append(random.randint(1,5))
        random_middle_marks.append(round(sum(random_marks)/len(random_marks),2))

    return random_marks, random_middle_marks

def recover_marks(middle_marks: list[int]) -> list[int]:
    cur_marks = []
    for i in range(len(middle_marks)):
        for j in range(1,6):
            if round((sum(cur_marks)+j)/(i+1),2) == middle_marks[i]:
                cur_marks.append(j)
                break

    return cur_marks

def test_work() -> bool:
    marks, middle_marks = generate_random_marks()
    recovered_marks = recover_marks(middle_marks)

    return marks==recovered_marks

def find_min_marks_optimized(marks, target, max_added=100):
    current_sum = sum(marks)
    current_count = len(marks)
    
    # Итерируемся по количеству добавляемых оценок (k)
    for k in range(1, max_added + 1):
        new_total_count = current_count + k
        
        # Границы суммы, которая даст нужный средний балл при округлении
        lower_bound = (target - 0.005) * new_total_count
        upper_bound = (target + 0.004999999) * new_total_count
        
        # Сумма, которую должны дать k новых оценок
        min_needed_sum = math.ceil(lower_bound - current_sum)
        max_needed_sum = math.floor(upper_bound - current_sum)
        
        # Проверяем, реально ли получить такую сумму k оценками (от 2 до 5)
        # Сумма k оценок всегда лежит в пределах [2*k, 5*k]
        possible_min = 2 * k
        possible_max = 5 * k
        
        actual_min = max(min_needed_sum, possible_min)
        actual_max = min(max_needed_sum, possible_max)
        
        if actual_min <= actual_max:
            # Мы нашли решение! Возьмем actual_min как целевую сумму.
            return marks + distribute_sum(actual_min, k)
            
    return None

def distribute_sum(total_sum, k):
    """Распределяет сумму total_sum на k слагаемых (от 2 до 5)"""
    base = total_sum // k
    remainder = total_sum % k
    # k - remainder оценок будут равны base, а remainder оценок будут равны base + 1
    marks = [base] * (k - remainder) + [base + 1] * remainder
    return marks

if __name__ == "__main__":
    # Тест: из [4] сделать 3.94
    # (4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 3.4) / 10 не выйдет, 
    # а вот (4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 3) / 10 = 3.9
    # Для 3.94 нужно больше оценок.
    print(find_min_marks_optimized([], 	3.6))

