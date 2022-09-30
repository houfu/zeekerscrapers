from dataclasses import dataclass, field
import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


@dataclass
class ZeekerItem:
    title: str
    published_date: str
    neutral_citation: str = ""
    file_urls: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)


class ZeekerModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    neutral_citation: str
    title: str
    published_date: str
