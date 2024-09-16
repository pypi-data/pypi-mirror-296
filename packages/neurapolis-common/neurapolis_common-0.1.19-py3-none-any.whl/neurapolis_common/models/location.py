from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class Location(BaseModel, RisApiDto, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    geojson: Optional[dict] = Field(default=None)
    street_address: Optional[str] = Field(default=None)
    room: Optional[str] = Field(default=None)
    postal_code: Optional[str] = Field(default=None)
    sub_locality: Optional[str] = Field(default=None)
    locality: Optional[str] = Field(default=None)
    bodies: Optional[list[str]] = Field(default=None)
    organizations: Optional[list[str]] = Field(default=None)
    persons: Optional[list[str]] = Field(default=None)
    meetings: Optional[list[str]] = Field(default=None)
    papers: Optional[list[str]] = Field(default=None)
    license: Optional[str] = Field(default=None)
    keyword: Optional[list[str]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, location_ris_api_dto: dict) -> "Location":
        return cls(
            id=location_ris_api_dto.get("id"),
            type=location_ris_api_dto.get("type"),
            description=location_ris_api_dto.get("description"),
            geojson=location_ris_api_dto.get("geojson"),
            street_address=location_ris_api_dto.get("streetAddress"),
            room=location_ris_api_dto.get("room"),
            postal_code=location_ris_api_dto.get("postalCode"),
            sub_locality=location_ris_api_dto.get("subLocality"),
            locality=location_ris_api_dto.get("locality"),
            bodies=location_ris_api_dto.get("bodies"),
            organizations=location_ris_api_dto.get("organizations"),
            persons=location_ris_api_dto.get("persons"),
            meetings=location_ris_api_dto.get("meetings"),
            papers=location_ris_api_dto.get("papers"),
            license=location_ris_api_dto.get("license"),
            keyword=location_ris_api_dto.get("keyword"),
            created=(
                None
                if location_ris_api_dto.get("created") == None
                else datetime.strptime(
                    location_ris_api_dto.get("created"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            modified=(
                None
                if location_ris_api_dto.get("modified") == None
                else datetime.strptime(
                    location_ris_api_dto.get("modified"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            web=location_ris_api_dto.get("web"),
            deleted=location_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "Location":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            description=db_node_dict.get("description"),
            # geojson=None,  # Not stored in DB
            street_address=db_node_dict.get("street_address"),
            room=db_node_dict.get("room"),
            postal_code=db_node_dict.get("postal_code"),
            sub_locality=db_node_dict.get("sub_locality"),
            locality=db_node_dict.get("locality"),
            # bodies=None, # Not stored in DB
            # organizations=None, # Not stored in DB
            # persons=None, # Not stored in DB
            # meetings=None, # Not stored in DB
            # papers=None, # Not stored in DB
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
            "description": self.description,
            "geojson": self.geojson,
            "street_address": self.street_address,
            "room": self.room,
            "postal_code": self.postal_code,
            "sub_locality": self.sub_locality,
            "locality": self.locality,
            "bodies": self.bodies,
            "organizations": self.organizations,
            "persons": self.persons,
            "meetings": self.meetings,
            "papers": self.papers,
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
            "description": self.description,
            # "geojson": self.geojson,
            "street_address": self.street_address,
            "room": self.room,
            "postal_code": self.postal_code,
            "sub_locality": self.sub_locality,
            "locality": self.locality,
            # "bodies": self.bodies,
            # "organizations": self.organizations,
            # "persons": self.persons,
            # "meetings": self.meetings,
            # "papers": self.papers,
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
            RetrieverLlmXmlField("description", self.description),
            RetrieverLlmXmlField("geojson", self.geojson),
            RetrieverLlmXmlField("street_address", self.street_address),
            RetrieverLlmXmlField("room", self.room),
            RetrieverLlmXmlField("postal_code", self.postal_code),
            RetrieverLlmXmlField("sub_locality", self.sub_locality),
            RetrieverLlmXmlField("locality", self.locality),
            # RetrieverLlmXmlField("bodies", self.bodies),
            # RetrieverLlmXmlField("organizations", self.organizations),
            # RetrieverLlmXmlField("persons", self.persons),
            # RetrieverLlmXmlField("meetings", self.meetings),
            # RetrieverLlmXmlField("papers", self.papers),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
