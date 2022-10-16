import datetime

import pytest

from pdpcSpider.items import CommissionDecisionItem, DecisionType, DPObligations


@pytest.fixture(name='decision')
def test_decision():
    test_summary_page = "https://www.pdpc.gov.sg/all-commissions-decisions/" \
                        "2022/07/breach-of-the-protection-obligation-by-crawfort"
    return CommissionDecisionItem(
        neutral_citation="", title="Breach of the Protection Obligation by Crawfort",
        published_date=datetime.date(2020, 10, 2).strftime('%d %B %Y'), summary_url=test_summary_page,
        decision=[DecisionType.DIRECTIONS], nature=[DPObligations.PROTECTION],
        respondent="Crawfort",
        decision_url="https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Commissions-Decisions/"
                     "Decision---Crawfort-Pte-Ltd---070622.ashx?la=en",
        summary="Directions were issued to Crawfort to conduct a security audit of its technical and "
                "administrative arrangements for its AWS S3 environment and rectify any security gaps "
                "identified in the audit report. This is pursuant to a data breach incident where "
                "Crawfort's customer database were offered for sale in the dark web."
    )


@pytest.mark.vcr
def test_CommissionDecisionSummaryPagePipeline_process_item():
    from pdpcSpider.pipelines import CommissionDecisionSummaryPagePipeline
    pipeline = CommissionDecisionSummaryPagePipeline()
    test_summary_page = "https://www.pdpc.gov.sg/all-commissions-decisions/" \
                        "2022/07/breach-of-the-protection-obligation-by-crawfort"
    test_item = CommissionDecisionItem(decision=[DecisionType.FINANCIAL_PENALTY],
                                       summary_url=test_summary_page,
                                       title="", nature=[], published_date="2 October 2020")
    test_item = pipeline.process_item(test_item, None)
    assert test_item.respondent == "Crawfort"
    assert test_item.summary == "Directions were issued to Crawfort to conduct a security audit of its technical and " \
                                "administrative arrangements for its AWS S3 environment and rectify any security gaps " \
                                "identified in the audit report. This is pursuant to a data breach incident where " \
                                "Crawfort's customer database were offered for sale in the dark web."
    assert test_item.decision_url == "https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Commissions-Decisions/" \
                                     "Decision---Crawfort-Pte-Ltd---070622.ashx?la=en"
    assert test_item.file_urls == ["https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Commissions-Decisions/"
                                   "Decision---Crawfort-Pte-Ltd---070622.ashx?la=en"]


@pytest.mark.default_cassette("test_CommissionDecisionSummaryPagePipeline_process_item.yaml")
@pytest.mark.vcr
def test_file_path():
    test_summary_page = "https://www.pdpc.gov.sg/all-commissions-decisions/" \
                        "2022/07/breach-of-the-protection-obligation-by-crawfort"
    test_item = CommissionDecisionItem(decision=[DecisionType.FINANCIAL_PENALTY],
                                       summary_url=test_summary_page,
                                       title="Breach of the Protection Obligation by Crawfort",
                                       nature=[], published_date="2 October 2020")
    from pdpcSpider.pipelines import PDPCDecisionDownloadFilePipeline
    pipeline = PDPCDecisionDownloadFilePipeline("dummy")
    from scrapy.http import TextResponse
    assert pipeline.file_path(TextResponse(""),
                              item=test_item) == 'full/2 October 2020 Breach of the Protection Obligation by Crawfort.pdf'


def test_PDPCDecisionAddToSQL_process_item(decision):
    from pdpcSpider.pipelines import PDPCDecisionAddToSQLPipeline
    pipeline = PDPCDecisionAddToSQLPipeline()
    pipeline.open_spider(None)
    pipeline.process_item(decision, None)
    from sqlmodel import Session
    from common.init_db import engine
    with Session(engine) as session:
        from sqlmodel import select
        from pdpcSpider.models import CommissionDecisionModel
        statement = select(CommissionDecisionModel)
        results = session.exec(statement)
        test = results.first().to_CommissionDecisionItem()
        assert test
        assert test.neutral_citation == ''
        assert test.title == decision.title
        assert test.published_date == decision.published_date
        assert test.summary_url == decision.summary_url
        assert test.nature == decision.nature
        assert test.decision == decision.decision
        assert test.respondent == decision.respondent
        assert test.decision_url == decision.decision_url
        assert test.summary == decision.summary


def test_PDPCDecisionDropDuplicates_process_item(decision):
    # First Add the Decision to database
    from pdpcSpider.pipelines import PDPCDecisionAddToSQLPipeline, PDPCDecisionDropDuplicatesPipeline
    sql_pipeline = PDPCDecisionAddToSQLPipeline()
    sql_pipeline.open_spider(None)
    sql_pipeline.process_item(decision, None)
    # Run the same decision through pipeline, check for drop
    pipeline = PDPCDecisionDropDuplicatesPipeline()
    pipeline.open_spider(None)
    from scrapy.exceptions import DropItem
    with pytest.raises(DropItem):
        pipeline.process_item(decision, None)
