from dataclasses import dataclass, field
from enum import Enum

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
    nature: list[DPObligations] = field(default_factory=list)
    decision: list[DecisionType] = field(default_factory=list)
    respondent: str = ""
    decision_url: str = ""
    summary: str = ""
