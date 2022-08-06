import datetime

import pytest

from pdpcSpider.items import CommissionDecisionItem, DecisionType


@pytest.mark.vcr
def test_CommissionDecisionSummaryPagePipeline_process_item():
    from pdpcSpider.pipelines import CommissionDecisionSummaryPagePipeline
    pipeline = CommissionDecisionSummaryPagePipeline()
    test_summary_page = "https://www.pdpc.gov.sg/all-commissions-decisions/" \
                        "2022/07/breach-of-the-protection-obligation-by-crawfort"
    test_item = CommissionDecisionItem(decision=[DecisionType.FINANCIAL_PENALTY],
                                       summary_url=test_summary_page,
                                       title="", nature="", published_date=datetime.date(2020, 10, 2))
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
