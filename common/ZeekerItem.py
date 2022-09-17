from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ZeekerItem:
    title: str
    published_date: datetime.date
    neutral_citation: str = ""
    file_urls: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
