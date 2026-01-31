def multiply(x, y):
    product = x * y
    return product

def get_first(items):
    if len(items) > 0:
        return items[0]
    return None

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

numbers = [5, 10, 15, 20, 25]
doubled = [n * 2 for n in numbers]

person = {
    'name': 'Bob',
    'age': 25,
    'city': 'Boston'
}

circle = Circle(5)
print(circle.area())
