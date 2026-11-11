"""Protocol
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from signalforge.models.research import Platform, RawResult
    from signalforge.pipeline.events import PipelineEvent


@runtime_checkable
class Serializable(Protocol):
    """

    """

    def to_dict(self) -> dict[str, Any]:
        """

        Returns:
        """
        ...


@runtime_checkable
class FileReader(Protocol):
    """"""

    def read(self, path: str) -> str:
        """

        Args:
            path: 

        Returns:
        """
        ...


@runtime_checkable
class AsyncFileReader(Protocol):
    """"""

    async def read(self, path: str) -> str:
        """

        Args:
            path: 

        Returns:
        """
        ...


@runtime_checkable
class FileWriter(Protocol):
    """"""

    def write(self, path: str, content: str) -> bool:
        """

        Args:
            path: 
            content: 

        Returns:
        """
        ...


@runtime_checkable
class AsyncFileWriter(Protocol):
    """"""

    async def write(self, path: str, content: str) -> bool:
        """

        Args:
            path: 
            content: 

        Returns:
        """
        ...


@runtime_checkable
class Closeable(Protocol):
    """"""

    def close(self) -> None:
        """"""
        ...


@runtime_checkable
class AsyncCloseable(Protocol):
    """"""

    async def close(self) -> None:
        """"""
        ...


@runtime_checkable
class Configurable(Protocol):
    """"""

    def configure(self, **kwargs: Any) -> None:
        """

        Args:
            **kwargs: 
        """
        ...


@runtime_checkable
class DataSource(Protocol):
    """Interface that all data source plugins must implement.

    """

    @property
    def platform(self) -> Platform:
        """Return the platform this source queries."""
        ...

    def is_available(self) -> bool:
        """Check if required credentials are configured."""
        ...

    async def search(self, queries: list[str], limit: int = 10) -> list[RawResult]:
        """Execute search and return raw results."""
        ...


@runtime_checkable
class ProgressCallback(Protocol):
    """Callback interface for receiving pipeline progress events."""

    async def on_event(self, event: PipelineEvent) -> None:
        """Handle a pipeline progress event."""
        ...


__all__ = [
    "Serializable",
    "FileReader",
    "AsyncFileReader",
    "FileWriter",
    "AsyncFileWriter",
    "Closeable",
    "AsyncCloseable",
    "Configurable",
    "DataSource",
    "ProgressCallback",
]
