from dataclasses import dataclass, field


@dataclass
class ZeekerItem:
    title: str
    published_date: str
    neutral_citation: str = ""
    file_urls: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
