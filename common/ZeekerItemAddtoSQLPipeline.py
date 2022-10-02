from sqlmodel import Session

from common.ZeekerItemModel import ZeekerItemModel
from common.init_db import engine, create_db_and_tables


class ZeekerItemAddToSQLPipeline:
    def __init__(self):
        self.engine = engine

    def open_spider(self, spider):
        create_db_and_tables()

    def process_item(self, item, spider):
        with Session(self.engine) as session:
            decision = ZeekerItemModel(
                neutral_citation=item.neutral_citation,
                title=item.title,
                published_date=item.published_date,
            )
            session.add(decision)
            session.commit()
