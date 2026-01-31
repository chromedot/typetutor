def count_items(items):
    total = 0
    for item in items:
        total += 1
    return total

def is_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def passed(self):
        return self.grade >= 60

colors = ['red', 'blue', 'green', 'yellow']
even_nums = [2, 4, 6, 8, 10]

for color in colors:
    print(color)

student = Student('Alice', 85)
print(student.passed())
