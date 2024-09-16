from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class LegislativeTerm(BaseModel, RisApiDto, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    body: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    license: Optional[str] = Field(default=None)
    keyword: Optional[list[str]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, legislative_term_ris_api_dto: dict) -> "LegislativeTerm":
        return cls(
            id=legislative_term_ris_api_dto.get("id"),
            url=legislative_term_ris_api_dto.get("url"),
            type=legislative_term_ris_api_dto.get("type"),
            body=legislative_term_ris_api_dto.get("body"),
            name=legislative_term_ris_api_dto.get("name"),
            start_date=(
                None
                if legislative_term_ris_api_dto.get("startDate") == None
                else datetime.fromisoformat(
                    legislative_term_ris_api_dto.get("startDate")
                )
            ),
            end_date=(
                None
                if legislative_term_ris_api_dto.get("endDate") == None
                else datetime.fromisoformat(legislative_term_ris_api_dto.get("endDate"))
            ),
            license=legislative_term_ris_api_dto.get("license"),
            keyword=legislative_term_ris_api_dto.get("keyword"),
            created=(
                None
                if legislative_term_ris_api_dto.get("created") == None
                else datetime.fromisoformat(legislative_term_ris_api_dto.get("created"))
            ),
            modified=(
                None
                if legislative_term_ris_api_dto.get("modified") == None
                else datetime.fromisoformat(
                    legislative_term_ris_api_dto.get("modified")
                )
            ),
            web=legislative_term_ris_api_dto.get("web"),
            deleted=legislative_term_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "LegislativeTerm":
        return cls(
            id=db_node_dict.get("id"),
            url=db_node_dict.get("url"),
            type=db_node_dict.get("type"),
            # body=None,  # Not stored in DB
            name=db_node_dict.get("name"),
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
            "url": self.url,
            "type": self.type,
            "body": self.body,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
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
            "url": self.url,
            "type": self.type,
            # "body": self.body,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
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
            # RetrieverLlmXmlField("url", self.url),
            # RetrieverLlmXmlField("type", self.type),
            # RetrieverLlmXmlField("body", self.body),
            RetrieverLlmXmlField("name", self.name),
            RetrieverLlmXmlField("start_date", self.start_date),
            RetrieverLlmXmlField("end_date", self.end_date),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
