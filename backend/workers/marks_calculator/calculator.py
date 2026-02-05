import random

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

if __name__ == "__main__":
    print(test_work())