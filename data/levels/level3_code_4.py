def reverse_string(text):
    return text[::-1]

def sum_list(numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.pages = 0

    def set_pages(self, num):
        self.pages = num

animals = ['cat', 'dog', 'bird']
scores = {
    'math': 90,
    'english': 85,
    'science': 92
}

book = Book('Python Guide', 'John Smith')
book.set_pages(250)
