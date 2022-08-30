import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Union


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
class CommissionDecisionItem:
    title: str
    summary_url: str
    nature: Union[list[DPObligations], str]
    decision: Union[list[DecisionType], str]
    published_date: datetime.date
    respondent: str = ""
    decision_url: str = ""
    summary: str = ""
    file_urls: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
