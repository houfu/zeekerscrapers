from typing import Optional

from sqlmodel import SQLModel, Field

from common.ZeekerItem import ZeekerItem


class ZeekerItemModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    neutral_citation: str
    title: str
    published_date: str

    def to_ZeekerItem(self):
        """
        A helper method is usually required to transform a SQL object model to an item for Scrapy.
        :return:
        """
        return ZeekerItem(
            neutral_citation=self.neutral_citation,
            title=self.title,
            published_date=self.published_date,
        )
