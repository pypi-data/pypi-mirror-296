from datetime import datetime
from typing import Optional


class RetrieverLlmXmlField:
    name: str
    value: Optional[str | int | float | datetime]

    def __init__(self, name: str, value: Optional[str | int | float | datetime]):
        self.name = name
        self.value = value
