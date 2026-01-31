# Web Security Fundamentals

## Common Vulnerabilities

Understanding security risks is the first step toward building secure applications.

### SQL Injection Prevention

Never concatenate user input directly into SQL queries. Use parameterized queries instead:

```python
# BAD - vulnerable to SQL injection
query = f"SELECT * FROM users WHERE email = '{user_email}'"

# GOOD - safe parameterized query
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (user_email,))
```

### XSS Protection

Always escape user-generated content before rendering:

```javascript
function sanitize(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}
```

## Authentication Best Practices

1. Hash passwords with `bcrypt` or `argon2`
2. Implement rate limiting on login endpoints
3. Use HTTPS for all authentication traffic

Stay vigilant and keep dependencies updated!
