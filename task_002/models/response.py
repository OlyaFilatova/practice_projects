from dataclasses import dataclass
from typing import Any


@dataclass
class Response:
    status: int
    headers: list[tuple[str, str]]
    body: list[Any]
