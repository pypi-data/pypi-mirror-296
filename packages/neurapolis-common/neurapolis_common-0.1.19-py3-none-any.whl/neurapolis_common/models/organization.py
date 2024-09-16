from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .location import Location
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class Organization(BaseModel, RisApiDto, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    body: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    membership: Optional[list[str]] = Field(default=None)
    meeting: Optional[str] = Field(default=None)
    consultation: Optional[str] = Field(default=None)
    short_name: Optional[str] = Field(default=None)
    post: Optional[list[str]] = Field(default=None)
    sub_organization_of: Optional[str] = Field(default=None)
    organization_type: Optional[str] = Field(default=None)
    classification: Optional[str] = Field(default=None)
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    website: Optional[str] = Field(default=None)
    location: Optional[Location] = Field(default=None)
    external_body: Optional[str] = Field(default=None)
    license: Optional[str] = Field(default=None)
    keyword: Optional[list[str]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, organization_ris_api_dto: dict) -> "Organization":
        return cls(
            id=organization_ris_api_dto.get("id"),
            type=organization_ris_api_dto.get("type"),
            body=organization_ris_api_dto.get("body"),
            name=organization_ris_api_dto.get("name"),
            membership=organization_ris_api_dto.get("membership", []),
            meeting=organization_ris_api_dto.get("meeting"),
            consultation=organization_ris_api_dto.get("consultation"),
            short_name=organization_ris_api_dto.get("shortName"),
            post=organization_ris_api_dto.get("post", []),
            sub_organization_of=organization_ris_api_dto.get("subOrganizationOf"),
            organization_type=organization_ris_api_dto.get("organizationType"),
            classification=organization_ris_api_dto.get("classification"),
            start_date=(
                None
                if organization_ris_api_dto.get("startDate") == None
                else datetime.fromisoformat(organization_ris_api_dto.get("startDate"))
            ),
            end_date=(
                None
                if organization_ris_api_dto.get("endDate") == None
                else datetime.fromisoformat(organization_ris_api_dto.get("endDate"))
            ),
            website=organization_ris_api_dto.get("website"),
            location=(
                Location.from_ris_api_dto(organization_ris_api_dto.get("location"))
                if organization_ris_api_dto.get("location")
                else None
            ),
            external_body=organization_ris_api_dto.get("externalBody"),
            license=organization_ris_api_dto.get("license"),
            keyword=organization_ris_api_dto.get("keyword", []),
            created=(
                None
                if organization_ris_api_dto.get("created") == None
                else datetime.strptime(
                    organization_ris_api_dto.get("created"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            modified=(
                None
                if organization_ris_api_dto.get("modified") == None
                else datetime.strptime(
                    organization_ris_api_dto.get("modified"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            web=organization_ris_api_dto.get("web"),
            deleted=organization_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "Organization":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            body=db_node_dict.get("body"),
            name=db_node_dict.get("name"),
            # membership=None,  # Not stored in DB
            # meeting=None,  # Not stored in DB
            # consultation=None,  # Not stored in DB
            short_name=db_node_dict.get("short_name"),
            post=db_node_dict.get("post"),
            # sub_organization_of=None,  # Not stored in DB
            organization_type=db_node_dict.get("organization_type"),
            classification=db_node_dict.get("classification"),
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
            website=db_node_dict.get("website"),
            # location=None,  # Not stored in DB
            external_body=db_node_dict.get("external_body"),
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
            "body": self.body,
            "name": self.name,
            "membership": self.membership,
            "meeting": self.meeting,
            "consultation": self.consultation,
            "short_name": self.short_name,
            "post": self.post,
            "sub_organization_of": self.sub_organization_of,
            "organization_type": self.organization_type,
            "classification": self.classification,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "website": self.website,
            "location": self.location.to_dict() if self.location else None,
            "external_body": self.external_body,
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
            "body": self.body,
            "name": self.name,
            # "membership": self.membership,
            # "meeting": self.meeting,
            # "consultation": self.consultation,
            "short_name": self.short_name,
            "post": self.post,
            # "sub_organization_of": self.sub_organization_of,
            "organization_type": self.organization_type,
            "classification": self.classification,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "website": self.website,
            # "location": self.location,
            "external_body": self.external_body,
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
            # RetrieverLlmXmlField("body", self.body),
            RetrieverLlmXmlField("name", self.name),
            # RetrieverLlmXmlField("membership", self.membership),
            # RetrieverLlmXmlField("meeting", self.meeting),
            # RetrieverLlmXmlField("consultation", self.consultation),
            RetrieverLlmXmlField("short_name", self.short_name),
            RetrieverLlmXmlField("post", self.post),
            # RetrieverLlmXmlField("sub_organization_of", self.sub_organization_of),
            RetrieverLlmXmlField("organization_type", self.organization_type),
            RetrieverLlmXmlField("classification", self.classification),
            RetrieverLlmXmlField("start_date", self.start_date),
            RetrieverLlmXmlField("end_date", self.end_date),
            RetrieverLlmXmlField("website", self.website),
            # RetrieverLlmXmlField("location", self.location),
            # RetrieverLlmXmlField("external_body", self.external_body),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
