from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class Consultation(BaseModel, RisApiDto, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    paper: Optional[str] = Field(default=None)
    agenda_item: Optional[str] = Field(default=None)
    meeting: Optional[str] = Field(default=None)
    organization: Optional[list[str]] = Field(default=None)
    authoritative: Optional[bool] = Field(default=None)
    role: Optional[str] = Field(default=None)
    license: Optional[str] = Field(default=None)
    keyword: Optional[list[str]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, consultation_ris_api_dto: dict) -> "Consultation":
        return cls(
            id=consultation_ris_api_dto.get("id"),
            type=consultation_ris_api_dto.get("type"),
            paper=consultation_ris_api_dto.get("paper"),
            agenda_item=consultation_ris_api_dto.get("agendaItem"),
            meeting=consultation_ris_api_dto.get("meeting"),
            organization=consultation_ris_api_dto.get("organization"),
            authoritative=consultation_ris_api_dto.get("authoritative"),
            role=consultation_ris_api_dto.get("role"),
            license=consultation_ris_api_dto.get("license"),
            keyword=consultation_ris_api_dto.get("keyword"),
            created=(
                None
                if consultation_ris_api_dto.get("created") == None
                else datetime.strptime(
                    consultation_ris_api_dto.get("created"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            modified=(
                None
                if consultation_ris_api_dto.get("modified") == None
                else datetime.strptime(
                    consultation_ris_api_dto.get("modified"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            web=consultation_ris_api_dto.get("web"),
            deleted=consultation_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "Consultation":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            # paper=None,  # Not stored in DB
            # agenda_item=None,  # Not stored in DB
            # meeting=None,  # Not stored in DB
            # organization=None,  # Not stored in DB
            authoritative=db_node_dict.get("authoritative"),
            role=db_node_dict.get("role"),
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
            "paper": self.paper,
            "agenda_item": self.agenda_item,
            "meeting": self.meeting,
            "organization": self.organization,
            "authoritative": self.authoritative,
            "role": self.role,
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
            # "paper": self.paper,
            # "agenda_item": self.agenda_item,
            # "meeting": self.meeting,
            # "organization": self.organization,
            "authoritative": self.authoritative,
            "role": self.role,
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
            # RetrieverLlmXmlField("paper", self.paper),
            # RetrieverLlmXmlField("agenda_item", self.agenda_item),
            # RetrieverLlmXmlField("meeting", self.meeting),
            # RetrieverLlmXmlField("organization", self.organization),
            # RetrieverLlmXmlField("authoritative", self.authoritative),
            RetrieverLlmXmlField("role", self.role),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
