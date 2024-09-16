from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .membership import Membership
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class Person(BaseModel, RisApiDto, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    body: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    family_name: Optional[str] = Field(default=None)
    given_name: Optional[str] = Field(default=None)
    form_of_address: Optional[str] = Field(default=None)
    affix: Optional[str] = Field(default=None)
    title: Optional[list[Optional[str]]] = Field(default=None)
    gender: Optional[str] = Field(default=None)
    phone: Optional[list[Optional[str]]] = Field(default=None)
    email: Optional[list[Optional[str]]] = Field(default=None)
    location: Optional[str] = Field(default=None)
    location_object: Optional[str] = Field(default=None)
    status: Optional[list[Optional[str]]] = Field(default=None)
    membership: Optional[list[Membership]] = Field(default=None)
    life: Optional[str] = Field(default=None)
    life_source: Optional[str] = Field(default=None)
    license: Optional[str] = Field(default=None)
    keyword: Optional[list[Optional[str]]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, person_ris_api_dto: dict) -> "Person":
        return cls(
            id=person_ris_api_dto.get("id"),
            type=person_ris_api_dto.get("type"),
            body=person_ris_api_dto.get("body"),
            name=person_ris_api_dto.get("name"),
            family_name=person_ris_api_dto.get("familyName"),
            given_name=person_ris_api_dto.get("givenName"),
            form_of_address=person_ris_api_dto.get("formOfAddress"),
            affix=person_ris_api_dto.get("affix"),
            title=person_ris_api_dto.get("title"),
            gender=person_ris_api_dto.get("gender"),
            phone=person_ris_api_dto.get("phone"),
            email=person_ris_api_dto.get("email"),
            location=person_ris_api_dto.get("location"),
            location_object=person_ris_api_dto.get("locationObject"),
            status=person_ris_api_dto.get("status"),
            membership=(
                [
                    Membership.from_ris_api_dto(x_membership_api_dto)
                    for x_membership_api_dto in person_ris_api_dto.get("membership")
                ]
                if person_ris_api_dto.get("membership")
                else None
            ),
            life=person_ris_api_dto.get("life"),
            life_source=person_ris_api_dto.get("lifeSource"),
            license=person_ris_api_dto.get("license"),
            keyword=person_ris_api_dto.get("keyword"),
            created=(
                None
                if person_ris_api_dto.get("created") == None
                else datetime.strptime(
                    person_ris_api_dto.get("created"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            modified=(
                None
                if person_ris_api_dto.get("modified") == None
                else datetime.strptime(
                    person_ris_api_dto.get("modified"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            web=person_ris_api_dto.get("web"),
            deleted=person_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "Person":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            # body=None,  # Not stored in DB
            name=db_node_dict.get("name"),
            family_name=db_node_dict.get("family_name"),
            given_name=db_node_dict.get("given_name"),
            form_of_address=db_node_dict.get("form_of_address"),
            affix=db_node_dict.get("affix"),
            title=db_node_dict.get("title"),
            gender=db_node_dict.get("gender"),
            phone=db_node_dict.get("phone"),
            email=db_node_dict.get("email"),
            # location=None,  # Not stored in DB
            # location_object=None,  # Not stored in DB
            status=db_node_dict.get("status"),
            # membership=None,  # Not stored in DB
            life=db_node_dict.get("life"),
            life_source=db_node_dict.get("life_source"),
            license=db_node_dict.get("license"),
            keyword=db_node_dict.get("keyword"),
            web=db_node_dict.get("web"),
            deleted=db_node_dict.get("deleted"),
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
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "body": self.body,
            "name": self.name,
            "family_name": self.family_name,
            "given_name": self.given_name,
            "form_of_address": self.form_of_address,
            "affix": self.affix,
            "title": self.title,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "location": self.location,
            "location_object": self.location_object,
            "status": self.status,
            "membership": (
                [membership.to_dict() for membership in self.membership]
                if self.membership
                else None
            ),
            "life": self.life,
            "life_source": self.life_source,
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
            # "body": self.body,
            "name": self.name,
            "family_name": self.family_name,
            "given_name": self.given_name,
            "form_of_address": self.form_of_address,
            "affix": self.affix,
            "title": self.title,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            # "location": self.location,
            # "location_object": self.location_object,
            "status": self.status,
            # "membership": self.membership,
            "life": self.life,
            "life_source": self.life_source,
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
            RetrieverLlmXmlField("family_name", self.family_name),
            RetrieverLlmXmlField("given_name", self.given_name),
            RetrieverLlmXmlField("form_of_address", self.form_of_address),
            RetrieverLlmXmlField("affix", self.affix),
            RetrieverLlmXmlField("title", self.title),
            RetrieverLlmXmlField("gender", self.gender),
            RetrieverLlmXmlField("phone", self.phone),
            RetrieverLlmXmlField("email", self.email),
            # RetrieverLlmXmlField("location", self.location),
            # RetrieverLlmXmlField("location_object", self.location_object),
            RetrieverLlmXmlField("status", self.status),
            # RetrieverLlmXmlField("membership", self.membership),
            RetrieverLlmXmlField("life", self.life),
            RetrieverLlmXmlField("life_source", self.life_source),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
