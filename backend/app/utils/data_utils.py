"""General data transformation helpers."""

from typing import Any, Generator, List


def chunk_list(items: List[Any], size: int) -> Generator[List[Any], None, None]:
    for i in range(0, len(items), size):
        yield items[i : i + size]
