def add_numbers(a, b):
    result = a + b
    return result

def find_max(numbers):
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    def display(self):
        print(f"{self.color} {self.brand}")

fruits = ['apple', 'banana', 'orange']
prices = {'apple': 1.50, 'banana': 0.75}

my_car = Car('Toyota', 'red')
my_car.display()
