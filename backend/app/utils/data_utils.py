"""General data transformation helpers."""

from collections.abc import Generator
from typing import Any


def chunk_list(items: list[Any], size: int) -> Generator[list[Any], None, None]:
    for i in range(0, len(items), size):
        yield items[i : i + size]
