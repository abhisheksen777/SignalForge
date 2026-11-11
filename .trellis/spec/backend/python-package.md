# Python Package Rules

## Package Shape

Use `src/signalforge/` for importable Python code and `tests/` for backend tests.
Do not import modules through `src.signalforge`.

Important stable surfaces:

- `signalforge.api.app:create_app`
- `signalforge.api.schemas`
- `signalforge.models.research`
- `signalforge.cache.base`
- `signalforge.config.settings.get_settings`

## Typing

- Keep `src/signalforge/py.typed`.
- Public functions need explicit return types.
- Use the project `BaseModel` from `signalforge.models.base` for reusable Pydantic
  models.
- Prefer `Protocol` when behavior contracts avoid coupling callers to a
  concrete implementation.
- Avoid `Any` unless the boundary is genuinely dynamic and narrowed promptly.

## Public API Changes

When adding or moving public symbols:

1. Update the relevant `__init__.py` export.
2. Update or add tests that import from the public surface.
3. Update docs that mention stable imports.
4. Run backend verification.
