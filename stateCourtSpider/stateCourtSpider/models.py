from typing import Optional

from sqlmodel import SQLModel, Field


class StateCourtDecisionItemModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    neutral_citation: str
    title: str
    published_date: str
