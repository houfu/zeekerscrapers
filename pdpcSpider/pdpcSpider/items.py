from dataclasses import dataclass
from enum import Enum
from typing import Union

from common.ZeekerItem import ZeekerItem


class DPObligations(Enum):
    ACCOUNTABILITY = "Accountability"
    CONSENT = "Consent"
    NOTIFICATION = "Notification"
    PROTECTION = "Protection"
    PURPOSE_LIMITATION = "Purpose Limitation"
    RETENTION_LIMITATION = "Retention Limitation"
    TRANSFER_LIMITATION = "Transfer Limitation"

    def __repr__(self):
        """Override default behaviour to just output the value"""
        return self.value


class DecisionType(Enum):
    ADVISORY_NOTICE = "Advisory Notice"
    DIRECTIONS = "Directions"
    FINANCIAL_PENALTY = "Financial Penalty"
    NOT_IN_BREACH = "Not in Breach"
    WARNING = "Warning"

    def __repr__(self):
        """Override default behaviour to just output the value"""
        return self.value


@dataclass
class CommissionDecisionItem(ZeekerItem):
    summary_url: str = ""
    nature: Union[list[DPObligations], str] = ""
    decision: Union[list[DecisionType], str] = ""
    respondent: str = ""
    decision_url: str = ""
    summary: str = ""
