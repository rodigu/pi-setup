---
name: python-skeleton
description: >
  Write Python function skeletons only - type hints, Google-style docstrings,
  descriptive names. No implementations. Use when user says "python skeleton",
  "function stubs", "scaffold functions", "write signatures", or invokes skill.
---

# python-skeleton

Write Python function skeletons only. No implementations.

## Activated When

User says: "python skeleton", "function stubs", "scaffold functions", "write signatures", `/skill:python-skeleton`

## Behavior

Generate Python functions with:

1. **Type hints** - all params + return type
2. **Google-style docstrings** - Args, Returns, Raises sections
3. **Descriptive names** - `calculate_monthly_revenue()` not `calc()`
4. **No body** - `pass` or ellipsis only

## Example Input

"Create skeleton for user authentication functions"

## Example Output

```python
def authenticate_user(username: str, password: str) -> dict:
    """Authenticate user credentials against database.

    Args:
        username: User's login name.
        password: Raw password string.

    Returns:
        Dict containing 'user_id', 'token', and 'expires_at'.

    Raises:
        AuthenticationError: If credentials invalid.
        DatabaseError: If connection fails.
    """
    pass


def validate_session_token(token: str) -> bool:
    """Check if session token is valid and not expired.

    Args:
        token: JWT session token string.

    Returns:
        True if token valid, False otherwise.
    """
    pass
```

## Rules

- No implementation logic
- No imports unless type hints need them (e.g., `Optional`, `List`)
- Use `pass` as placeholder
- Include Raises section when errors likely
- One blank line between functions
- Keep docstrings concise - no examples unless user requests
- Class methods: include `self` param with no type hint

## Exclusions

Do NOT:
- Write actual logic
- Add TODO comments
- Create full modules with imports
- Generate test code
