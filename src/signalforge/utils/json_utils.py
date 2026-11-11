"""JSON utilities module."""

import asyncio
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import aiofiles

from signalforge.observability.log_config import get_logger
from signalforge.utils.decorator_utils import timing

logger = get_logger(__name__)


# =============================================================================
#  JSON 
# =============================================================================


@timing
def read_json(
    file_path: str | Path,
    encoding: str = "utf-8",
    default: dict[str, Any] | list[Any] | None = None,
) -> dict[str, Any] | list[Any] | None:
    """ JSON 

    Args:
        file_path: JSON 
        encoding: 
        default: 

    Returns:
        dict | list | None:  JSON  default
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return default

        with open(file_path, encoding=encoding) as f:
            data = json.load(f)
            logger.debug(f"Read JSON from: {file_path}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {file_path}: {e}")
        return default
    except Exception as e:
        logger.error(f"Failed to read JSON file {file_path}: {e}")
        return default


@timing
def write_json(
    data: Any,
    file_path: str | Path,
    encoding: str = "utf-8",
    indent: int = 2,
    ensure_ascii: bool = False,
    create_dirs: bool = True,
    **kwargs: Any,
) -> bool:
    """ JSON 

    Args:
        data: 
        file_path: JSON 
        encoding: 
        indent: 
        ensure_ascii:  ASCII 
        create_dirs: 
        **kwargs:  json.dumps 

    Returns:
        bool:  True False
    """
    try:
        file_path = Path(file_path)

        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)

        json_str = json.dumps(
            data,
            indent=indent,
            ensure_ascii=ensure_ascii,
            **kwargs,
        )

        with open(file_path, "w", encoding=encoding) as f:
            f.write(json_str)

        logger.debug(f"Wrote JSON to: {file_path}")
        return True
    except TypeError as e:
        logger.error(f"JSON serialization error: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to write JSON file {file_path}: {e}")
        return False


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """ JSON 

    Args:
        json_str: JSON 
        default: 

    Returns:
    """
    try:
        return json.loads(json_str)
    except (TypeError, json.JSONDecodeError):
        return default


def safe_json_dumps(
    obj: Any,
    default: Callable[[Any], Any] | None = None,
    indent: int | None = 2,
    fallback: str | None = None,
    ensure_ascii: bool = False,
    **kwargs: Any,
) -> str | None:
    """ JSON

    Args:
        obj: 
        default:  json.dumps 
        indent: 
        fallback: 
        ensure_ascii:  ASCII
        **kwargs:  json.dumps 

    Returns:
        str | None:  JSON 
    """
    try:
        return json.dumps(
            obj,
            default=default,
            indent=indent,
            ensure_ascii=ensure_ascii,
            **kwargs,
        )
    except TypeError as e:
        logger.error(f"JSON serialization error: {e}")
        return fallback
    except Exception as e:
        logger.error(f"Failed to serialize JSON: {e}")
        return fallback


@timing
def merge_json_files(
    file_paths: list[str | Path],
    output_path: str | Path | None = None,
) -> dict[str, Any] | None:
    """ JSON 

    Args:
        file_paths: JSON 
        output_path: ()

    Returns:
        dict | None:  None
    """
    merged: dict[str, Any] = {}

    for path in file_paths:
        data = read_json(path)
        if data is None:
            logger.error(f"Failed to read {path}")
            return None

        if isinstance(data, dict):
            merged.update(data)
        else:
            logger.warning(f"Skipping non-dict JSON file: {path}")

    if output_path and not write_json(merged, output_path):
        logger.error(f"Failed to write merged JSON to {output_path}")
        return None

    return merged


def pretty_print_json(data: Any, indent: int = 2) -> None:
    """ JSON 

    Args:
        data: 
        indent: 
    """
    try:
        print(json.dumps(data, indent=indent, ensure_ascii=False))
    except TypeError as e:
        logger.error(f"Failed to pretty print JSON: {e}")
        print(str(data))


def validate_json_schema(
    data: dict[str, Any],
    required_keys: list[str],
) -> bool:
    """ JSON 

    Args:
        data: 
        required_keys: 

    Returns:
        bool:  True
    """
    missing_keys = [key for key in required_keys if key not in data]

    if missing_keys:
        logger.error(f"Missing required keys: {missing_keys}")
        return False

    return True


def json_path_get(
    data: dict[str, Any] | list[Any],
    path: str,
    separator: str = ".",
) -> Any | None:
    """ JSON 

    Args:
        data: JSON 
        path:  ( "a.b.c"  "items.0.name")
        separator: 

    Returns:
        Any | None:  None
    """
    keys = path.split(separator)
    current: Any = data

    try:
        for key in keys:
            if isinstance(current, dict):
                if key in current:
                    current = current[key]
                else:
                    return None
            elif isinstance(current, list):
                index = int(key)
                if 0 <= index < len(current):
                    current = current[index]
                else:
                    return None
            else:
                return None
        return current
    except Exception:
        return None


# =============================================================================
#  JSON 
# =============================================================================


async def async_read_json(
    file_path: str | Path,
    encoding: str = "utf-8",
) -> dict[str, Any] | list[Any] | None:
    """ JSON 

    Args:
        file_path: JSON 
        encoding: 

    Returns:
        dict | list | None:  JSON  None
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None

        async with aiofiles.open(file_path, encoding=encoding) as f:
            content = await f.read()
            data = json.loads(content)
            logger.debug(f"Async read JSON from: {file_path}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to read JSON file {file_path}: {e}")
        return None


async def async_write_json(
    data: Any,
    file_path: str | Path,
    encoding: str = "utf-8",
    indent: int = 2,
    ensure_ascii: bool = False,
    create_dirs: bool = True,
) -> bool:
    """ JSON 

    Args:
        data: 
        file_path: JSON 
        encoding: 
        indent: 
        ensure_ascii:  ASCII 
        create_dirs: 

    Returns:
        bool:  True False
    """
    try:
        file_path = Path(file_path)

        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)

        json_str = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)

        async with aiofiles.open(file_path, "w", encoding=encoding) as f:
            await f.write(json_str)

        logger.debug(f"Async wrote JSON to: {file_path}")
        return True
    except TypeError as e:
        logger.error(f"JSON serialization error: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to write JSON file {file_path}: {e}")
        return False


async def async_merge_json_files(
    file_paths: list[str | Path],
    output_path: str | Path | None = None,
) -> dict[str, Any] | None:
    """ JSON 

    Args:
        file_paths: JSON 
        output_path: ()

    Returns:
        dict | None:  None
    """
    merged: dict[str, Any] = {}

    for path in file_paths:
        data = await async_read_json(path)
        if data is None:
            logger.error(f"Failed to read {path}")
            return None

        if isinstance(data, dict):
            merged.update(data)
        else:
            logger.warning(f"Skipping non-dict JSON file: {path}")

    if output_path:
        write_ok = await async_write_json(merged, output_path)
        if not write_ok:
            logger.error(f"Failed to write merged JSON to {output_path}")
            return None

    return merged


async def async_load_json_batch(
    file_paths: list[str | Path],
    max_concurrency: int = 5,
) -> list[dict[str, Any] | list[Any] | None]:
    """ JSON 

    Args:
        file_paths: JSON 
        max_concurrency: 

    Returns:
         ( None)
    """
    semaphore = asyncio.Semaphore(max_concurrency)

    async def load_with_semaphore(
        path: str | Path,
    ) -> dict[str, Any] | list[Any] | None:
        async with semaphore:
            return await async_read_json(path)

    tasks = [load_with_semaphore(path) for path in file_paths]
    return await asyncio.gather(*tasks)


__all__ = [
    "read_json",
    "write_json",
    "safe_json_loads",
    "safe_json_dumps",
    "merge_json_files",
    "pretty_print_json",
    "validate_json_schema",
    "json_path_get",
    "async_read_json",
    "async_write_json",
    "async_merge_json_files",
    "async_load_json_batch",
]
