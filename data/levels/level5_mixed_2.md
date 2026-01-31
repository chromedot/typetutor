# Database Query Optimization Guide

## Introduction

Optimizing database queries is essential for application performance. This guide covers common patterns and best practices.

## Indexing Strategies

When creating indexes, consider the query patterns your application uses most frequently. Here's an example of creating a compound index:

```sql
CREATE INDEX idx_user_activity
ON users (last_login DESC, account_status);
```

## Query Examples

### Finding Active Users

```python
def get_active_users(db, days=30):
    cutoff = datetime.now() - timedelta(days=days)
    return db.query(User).filter(
        User.last_login >= cutoff,
        User.status == 'active'
    ).all()
```

## Best Practices

1. **Use connection pooling** to reduce overhead
2. **Avoid N+1 queries** by using joins or eager loading
3. **Monitor slow queries** with logging enabled

Remember to test with production-like data volumes!
