def test_pipeline():
    from common.ZeekerItemAddtoSQLPipeline import ZeekerItemAddToSQLPipeline
    pipeline = ZeekerItemAddToSQLPipeline()
    pipeline.open_spider(None)
    from common.ZeekerItem import ZeekerItem
    pipeline.process_item(ZeekerItem(
        published_date="3 October 2022",
        neutral_citation="[2022] Test 1",
        title="Test Zeeker Item"
    ), None)
    from common.init_db import engine
    from sqlmodel import Session
    with Session(engine) as session:
        from sqlmodel import select
        from common.ZeekerItemModel import ZeekerItemModel
        statement = select(ZeekerItemModel)
        result = session.exec(statement)
        test = result.first().to_ZeekerItem()
        assert test
        assert test.neutral_citation == '[2022] Test 1'
        assert test.title == "Test Zeeker Item"
        assert test.published_date == "3 October 2022"
