"""Context management for storing runtime values.

This module provides an async-safe context system using contextvars for storing
and managing runtime values. Supports scoped contexts and hierarchical context
management with proper isolation between async tasks.
"""

from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager
from contextvars import Context as ContextRunner
from contextvars import ContextVar
from typing import Any, TypeVar

T = TypeVar("T")

_context_data: ContextVar[dict[str, Any] | None] = ContextVar(
    "context_data", default=None
)
_named_contexts: ContextVar[dict[str, "Context"] | None] = ContextVar(
    "named_contexts", default=None
)


class Context:
    """Async-safe context for storing runtime values.


    This class uses contextvars internally, providing proper isolation between
    different async tasks while maintaining a simple dictionary-like interface.

     contextvars

    Example:
        >>> ctx = Context()
        >>> ctx.set("user_id", 123)
        >>> ctx.get("user_id")
        123
        >>> ctx.get("missing", "default")
        'default'
    """

    def __init__(self, name: str = "default") -> None:
        """Initialize context.


        Args:
            name: Context name for identification
        """
        self.name = name
        self._data: ContextVar[dict[str, Any] | None] = ContextVar(
            f"context_{name}", default=None
        )

    def _get_data(self) -> dict[str, Any]:
        """"""
        data = self._data.get()
        if data is None:
            data = {}
            self._data.set(data)
        return data

    def set(self, key: str, value: Any) -> None:
        """Set a value in the context.


        Args:
            key: Key to store value under
            value: Value to store
        """
        data = self._get_data().copy()
        data[key] = value
        self._data.set(data)

    def get(self, key: str, default: T | None = None) -> T | None:
        """Get a value from the context.


        Args:
            key: Key to retrieve
            default: Default value if key not found

        Returns:
            Value associated with key, or default if not found
        """
        return self._get_data().get(key, default)

    def delete(self, key: str) -> bool:
        """Delete a value from the context.


        Args:
            key: Key to delete

        Returns:
            True if key was deleted, False if key didn't exist
        """
        data = self._get_data()
        if key in data:
            new_data = data.copy()
            del new_data[key]
            self._data.set(new_data)
            return True
        return False

    def has(self, key: str) -> bool:
        """Check if a key exists in the context.


        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise
        """
        return key in self._get_data()

    def clear(self) -> None:
        """Clear all values from the context.

        """
        self._data.set({})

    def keys(self) -> list[str]:
        """Get all keys in the context.


        Returns:
            List of all keys
        """
        return list(self._get_data().keys())

    def values(self) -> list[Any]:
        """Get all values in the context.


        Returns:
            List of all values
        """
        return list(self._get_data().values())

    def items(self) -> list[tuple[str, Any]]:
        """Get all key-value pairs in the context.


        Returns:
            List of (key, value) tuples
        """
        return list(self._get_data().items())

    def update(self, data: dict[str, Any]) -> None:
        """Update context with multiple key-value pairs.


        Args:
            data: Dictionary of key-value pairs to add
        """
        new_data = self._get_data().copy()
        new_data.update(data)
        self._data.set(new_data)

    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary.


        Returns:
            Copy of internal data dictionary
        """
        return self._get_data().copy()

    def __len__(self) -> int:
        """Get number of items in context.

        """
        return len(self._get_data())

    def __repr__(self) -> str:
        """String representation of context.

        """
        return f"Context(name='{self.name}', items={len(self)})"

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator."""
        return self.has(key)

    def __getitem__(self, key: str) -> Any:
        """Support bracket notation for getting values."""
        value = self.get(key)
        if value is None and key not in self._get_data():
            raise KeyError(key)
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        """Support bracket notation for setting values."""
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        """Support bracket notation for deleting values."""
        if not self.delete(key):
            raise KeyError(key)


class ContextManager:
    """Manager for multiple context scopes.


    This class manages multiple named contexts and provides utilities for
    working with scoped contexts.


    Example:
        >>> manager = ContextManager()
        >>> ctx = manager.get_or_create_context("request")
        >>> ctx.set("user", "alice")
        >>> ctx.get("user")
        'alice'
    """

    def __init__(self) -> None:
        """Initialize context manager.

        """
        self._contexts: dict[str, Context] = {}

    def create_context(self, name: str) -> Context:
        """Create a new named context.


        Args:
            name: Name for the new context

        Returns:
            Newly created context

        Raises:
            ValueError: If context with this name already exists
        """
        if name in self._contexts:
            raise ValueError(f"Context '{name}' already exists")
        ctx = Context(name=name)
        self._contexts[name] = ctx
        return ctx

    def get_context(self, name: str) -> Context | None:
        """Get a context by name.


        Args:
            name: Name of context to retrieve

        Returns:
            Context if found, None otherwise
        """
        return self._contexts.get(name)

    def get_or_create_context(self, name: str) -> Context:
        """Get existing context or create new one.


        Args:
            name: Name of context

        Returns:
            Existing or newly created context
        """
        if name not in self._contexts:
            self._contexts[name] = Context(name=name)
        return self._contexts[name]

    def delete_context(self, name: str) -> bool:
        """Delete a context by name.


        Args:
            name: Name of context to delete

        Returns:
            True if context was deleted, False if it didn't exist
        """
        if name in self._contexts:
            del self._contexts[name]
            return True
        return False

    def clear_all(self) -> None:
        """Clear all contexts.

        """
        self._contexts.clear()

    def list_contexts(self) -> list[str]:
        """List all context names.


        Returns:
            List of context names
        """
        return list(self._contexts.keys())


# Global instances / 
_global_context: Context | None = None
_context_manager: ContextManager | None = None


def get_context(name: str = "global") -> Context:
    """Get or create a global context.


    Args:
        name: Context name (default: "global")

    Returns:
        Context instance

    Example:
        >>> ctx = get_context()
        >>> ctx.set("app_start_time", time.time())
    """
    global _context_manager
    if _context_manager is None:
        _context_manager = ContextManager()
    return _context_manager.get_or_create_context(name)


def get_global_context() -> Context:
    """Get the global application context.


    Returns:
        Global context instance
    """
    global _global_context
    if _global_context is None:
        _global_context = Context(name="global")
    return _global_context


@contextmanager
def context_scope(
    name: str, initial_data: dict[str, Any] | None = None
) -> Generator[Context, None, None]:
    """Context manager for scoped context operations.


    Creates a temporary context that is automatically cleaned up when exiting
    the scope. Useful for request/session-scoped data.

    /

    Args:
        name: Name for the scoped context
        initial_data: Optional initial data to populate context

    Yields:
        Context instance for the scope

    Example:
        >>> with context_scope("request", {"user_id": 123}) as ctx:
        ...     ctx.set("action", "login")
        ...     print(ctx.get("user_id"))
        123
        # Context is automatically cleaned up after exiting
    """
    ctx = get_context(name)
    if initial_data:
        ctx.update(initial_data)
    try:
        yield ctx
    finally:
        global _context_manager
        if _context_manager:
            _context_manager.delete_context(name)


@asynccontextmanager
async def async_context_scope(
    name: str, initial_data: dict[str, Any] | None = None
) -> AsyncGenerator[Context, None]:
    """Async context manager for scoped context operations.


    Args:
        name: Name for the scoped context
        initial_data: Optional initial data to populate context

    Yields:
        Context instance for the scope

    Example:
        >>> async with async_context_scope("request", {"user_id": 123}) as ctx:
        ...     ctx.set("action", "login")
        ...     print(ctx.get("user_id"))
        123
    """
    ctx = get_context(name)
    if initial_data:
        ctx.update(initial_data)
    try:
        yield ctx
    finally:
        global _context_manager
        if _context_manager:
            _context_manager.delete_context(name)


def run_in_context(ctx: Context, func: Any, *args: Any, **kwargs: Any) -> Any:
    """Run a function with a specific context.


    Args:
        ctx: Context to use
        func: Function to run
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Function result
    """
    data_snapshot = ctx.to_dict()
    execution_context = ContextRunner()
    execution_context.run(ctx._data.set, data_snapshot)
    return execution_context.run(func, *args, **kwargs)


# Convenience functions / 
def set_global(key: str, value: Any) -> None:
    """Set a value in the global context.


    Args:
        key: Key to store value under
        value: Value to store
    """
    get_global_context().set(key, value)


def get_global(key: str, default: T | None = None) -> T | None:
    """Get a value from the global context.


    Args:
        key: Key to retrieve
        default: Default value if key not found

    Returns:
        Value associated with key, or default if not found
    """
    return get_global_context().get(key, default)


def clear_global() -> None:
    """Clear the global context.

    """
    get_global_context().clear()


__all__ = [
    "Context",
    "ContextManager",
    "get_context",
    "get_global_context",
    "context_scope",
    "async_context_scope",
    "run_in_context",
    "set_global",
    "get_global",
    "clear_global",
]
