import pytest
import requests

from stateCourtSpider.spiders.latestJudgmentsStateCourtSpider import LatestJudgmentsStateCourtSpider


def test_start_url():
    spider = LatestJudgmentsStateCourtSpider()
    response = requests.get(spider.start_urls[0])
    assert response.status_code == 200
