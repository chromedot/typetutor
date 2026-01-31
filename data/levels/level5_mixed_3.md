# Testing Best Practices

## Unit Testing Basics

Writing effective unit tests requires understanding what to test and how to structure your tests for maintainability.

### Example Test Class

```python
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_addition(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
```

## Mocking External Dependencies

Use mocks to isolate the code under test:

```python
from unittest.mock import patch, MagicMock

@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {'status': 'ok'}
    response = fetch_data('https://api.example.com')
    assert response['status'] == 'ok'
```

**Key Principle**: Test behavior, not implementation details.
