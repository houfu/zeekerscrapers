from typing import Optional, List

from sqlmodel import SQLModel, Field, Session, Relationship

from common.init_db import engine
from pdpcSpider.items import CommissionDecisionItem, DPObligations, DecisionType


class DecisionTypeModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: DecisionType = Field(index=True)


class DecisionTypeLink(SQLModel, table=True):
    decision_id: Optional[int] = Field(
        default=None, foreign_key="commissiondecisionmodel.id", primary_key=True,
    )
    decisiontype_id: Optional[int] = Field(
        default=None, foreign_key="decisiontypemodel.id", primary_key=True
    )


def create_DecisionType():
    with Session(engine) as session:
        for nature in DecisionType:
            session.add(DecisionTypeModel(value=nature))
        session.commit()


class DPObligationsModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: DPObligations = Field(index=True)


class DPObligationsLink(SQLModel, table=True):
    decision_id: Optional[int] = Field(
        default=None, foreign_key="commissiondecisionmodel.id", primary_key=True,
    )
    dpobligations_id: Optional[int] = Field(
        default=None, foreign_key="dpobligationsmodel.id", primary_key=True
    )


def create_DPObligations():
    with Session(engine) as session:
        for obligation in DPObligations:
            session.add(DPObligationsModel(value=obligation))
        session.commit()


class CommissionDecisionModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    neutral_citation: str
    title: str
    published_date: str
    summary_url: str
    nature: List[DPObligationsModel] = Relationship(link_model=DPObligationsLink)
    decision: List[DecisionTypeModel] = Relationship(link_model=DecisionTypeLink)
    respondent: str
    decision_url: str
    summary: str

    def to_CommissionDecisionItem(self) -> CommissionDecisionItem:
        return CommissionDecisionItem(
            neutral_citation=self.neutral_citation,
            title=self.title,
            published_date=self.published_date,
            summary_url=self.summary_url,
            summary=self.summary,
            decision_url=self.decision_url,
            respondent=self.respondent,
            nature=[obligation.value for obligation in self.nature],
            decision=[decision.value for decision in self.decision]
        )
