def calculate_total(items):
    total = 0
    for item in items:
        total += item['price']
    return total

def greet(name):
    message = f"Hello, {name}!"
    print(message)
    return message

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

numbers = [1, 2, 3, 4, 5]
squares = [n * n for n in numbers]

user_data = {
    'name': 'Alice',
    'age': 30,
    'active': True
}
