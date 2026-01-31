# API Documentation

## Authentication

All API requests require authentication using a bearer token:

```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_TOKEN_HERE',
    'Content-Type': 'application/json'
}

response = requests.get('https://api.example.com/users', headers=headers)
```

## Endpoints

### GET /users

Retrieves a list of users. Supports pagination via `?page=1&limit=10` query parameters.

**Example response:**

```json
{
    "users": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ],
    "total": 42
}
```

### POST /users

Creates a new user. Requires `name` and `email` fields in the request body.

**Important:** Email addresses must be unique and properly formatted.

The API will return `400 Bad Request` if validation fails, or `201 Created` on success with the new user object.
