def test_dpobligations():
    from pdpcSpider.items import DPObligations
    assert repr(DPObligations.CONSENT) == 'Consent'


def test_decision_type():
    from pdpcSpider.items import DecisionType
    test = DecisionType.FINANCIAL_PENALTY
    assert repr(test) == "Financial Penalty"
