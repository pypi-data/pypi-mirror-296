from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class Membership(BaseModel, RisApiDto, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    person: Optional[str] = Field(default=None)
    organization: Optional[str] = Field(default=None)
    role: Optional[str] = Field(default=None)
    voting_right: Optional[bool] = Field(default=None)
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    on_behalf_of: Optional[str] = Field(default=None)
    license: Optional[str] = Field(default=None)
    keyword: Optional[list[str]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, membership_ris_api_dto: dict) -> "Membership":
        return cls(
            id=membership_ris_api_dto.get("id"),
            type=membership_ris_api_dto.get("type"),
            person=membership_ris_api_dto.get("person"),
            organization=membership_ris_api_dto.get("organization"),
            role=membership_ris_api_dto.get("role"),
            voting_right=membership_ris_api_dto.get("votingRight"),
            start_date=(
                None
                if membership_ris_api_dto.get("startDate") == None
                else datetime.fromisoformat(membership_ris_api_dto.get("startDate"))
            ),
            end_date=(
                None
                if membership_ris_api_dto.get("endDate") == None
                else datetime.fromisoformat(membership_ris_api_dto.get("endDate"))
            ),
            on_behalf_of=membership_ris_api_dto.get("onBehalfOf"),
            license=membership_ris_api_dto.get("license"),
            keyword=membership_ris_api_dto.get("keyword"),
            created=(
                None
                if membership_ris_api_dto.get("created") == None
                else datetime.strptime(
                    membership_ris_api_dto.get("created"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            modified=(
                None
                if membership_ris_api_dto.get("modified") == None
                else datetime.strptime(
                    membership_ris_api_dto.get("modified"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            web=membership_ris_api_dto.get("web"),
            deleted=membership_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "Membership":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            # person=None,  # Not stored in DB
            # organization=None,  # Not stored in DB
            role=db_node_dict.get("role"),
            voting_right=db_node_dict.get("voting_right"),
            start_date=(
                None
                if db_node_dict.get("start_date") == None
                else datetime.fromtimestamp(
                    db_node_dict.get("start_date").to_native().timestamp()
                )
            ),
            end_date=(
                None
                if db_node_dict.get("end_date") == None
                else datetime.fromtimestamp(
                    db_node_dict.get("end_date").to_native().timestamp()
                )
            ),
            # on_behalf_of=None,  # Not stored in DB
            license=db_node_dict.get("license"),
            keyword=db_node_dict.get("keyword"),
            created=(
                None
                if db_node_dict.get("created") == None
                else datetime.fromtimestamp(
                    db_node_dict.get("created").to_native().timestamp()
                )
            ),
            modified=(
                None
                if db_node_dict.get("modified") == None
                else datetime.fromtimestamp(
                    db_node_dict.get("modified").to_native().timestamp()
                )
            ),
            web=db_node_dict.get("web"),
            deleted=db_node_dict.get("deleted"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "person": self.person,
            "organization": self.organization,
            "role": self.role,
            "voting_right": self.voting_right,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "on_behalf_of": self.on_behalf_of,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }

    def to_db_node_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            # "person": self.person,
            # "organization": self.organization,
            "role": self.role,
            "voting_right": self.voting_right,
            "start_date": self.start_date,
            "end_date": self.end_date,
            # "on_behalf_of": self.on_behalf_of,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }

    def get_llm_xml_fields(self) -> list[RetrieverLlmXmlField]:
        return [
            RetrieverLlmXmlField("id", self.id),
            # RetrieverLlmXmlField("type", self.type),
            # RetrieverLlmXmlField("person", self.person),
            # RetrieverLlmXmlField("organization", self.organization),
            RetrieverLlmXmlField("role", self.role),
            RetrieverLlmXmlField("voting_right", self.voting_right),
            RetrieverLlmXmlField("start_date", self.start_date),
            RetrieverLlmXmlField("end_date", self.end_date),
            # RetrieverLlmXmlField("on_behalf_of", self.on_behalf_of),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
