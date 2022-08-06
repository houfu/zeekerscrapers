import pytest


@pytest.mark.vcr
def test_start_url():
    import requests
    from pdpcSpider.spiders.CommissionDecisionSpider import CASE_LISTING_URL
    from pdpcSpider.spiders.CommissionDecisionSpider import create_form_data
    response = requests.post(CASE_LISTING_URL, data=create_form_data(1))
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["ResponseCode"] == "OK"
