from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .legislative_term import LegislativeTerm
from .location import Location
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class Body(
    BaseModel,
    RisApiDto,
    DbNodeDict,
    RetrieverState,
):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    system: Optional[str] = Field(default=None)
    short_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    license: Optional[str] = Field(default=None)
    license_valid_since: Optional[datetime] = Field(default=None)
    oparl_since: Optional[datetime] = Field(default=None)
    ags: Optional[str] = Field(default=None)
    rgs: Optional[str] = Field(default=None)
    equivalent: Optional[list[str]] = Field(default=None)
    contact_email: Optional[str] = Field(default=None)
    contact_name: Optional[str] = Field(default=None)
    organization: Optional[str] = Field(default=None)
    person: Optional[str] = Field(default=None)
    meeting: Optional[str] = Field(default=None)
    paper: Optional[str] = Field(default=None)
    legislative_term: Optional[list[LegislativeTerm]] = Field(default=None)
    agenda_item: Optional[str] = Field(default=None)
    consultation: Optional[str] = Field(default=None)
    file: Optional[str] = Field(default=None)
    location_list: Optional[str] = Field(default=None)
    legislative_term_list: Optional[str] = Field(default=None)
    membership: Optional[str] = Field(default=None)
    classification: Optional[str] = Field(default=None)
    location: Optional[Location] = Field(default=None)
    keyword: Optional[list[str]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, body_ris_api_dto: dict) -> "Body":
        return cls(
            id=body_ris_api_dto.get("id"),
            type=body_ris_api_dto.get("type"),
            system=body_ris_api_dto.get("system"),
            short_name=body_ris_api_dto.get("shortName"),
            name=body_ris_api_dto.get("name"),
            website=body_ris_api_dto.get("website"),
            license=body_ris_api_dto.get("license"),
            license_valid_since=(
                None
                if body_ris_api_dto.get("licenseValidSince") == None
                else datetime.fromisoformat(body_ris_api_dto.get("licenseValidSince"))
            ),
            oparl_since=(
                None
                if body_ris_api_dto.get("oparlSince") == None
                else datetime.fromisoformat(body_ris_api_dto.get("oparlSince"))
            ),
            ags=body_ris_api_dto.get("ags"),
            rgs=body_ris_api_dto.get("rgs"),
            equivalent=body_ris_api_dto.get("equivalent"),
            contact_email=body_ris_api_dto.get("contactEmail"),
            contact_name=body_ris_api_dto.get("contactName"),
            organization=body_ris_api_dto.get("organization"),
            person=body_ris_api_dto.get("person"),
            meeting=body_ris_api_dto.get("meeting"),
            paper=body_ris_api_dto.get("paper"),
            legislative_term=(
                [
                    LegislativeTerm.from_ris_api_dto(x_legislative_term_ris_api_dto)
                    for x_legislative_term_ris_api_dto in body_ris_api_dto.get(
                        "legislativeTerm"
                    )
                ]
                if body_ris_api_dto.get("legislativeTerm")
                else None
            ),
            agenda_item=body_ris_api_dto.get("agendaItem"),
            consultation=body_ris_api_dto.get("consultation"),
            file=body_ris_api_dto.get("file"),
            location_list=body_ris_api_dto.get("locationList"),
            legislative_term_list=body_ris_api_dto.get("legislativeTermList"),
            membership=body_ris_api_dto.get("membership"),
            classification=body_ris_api_dto.get("classification"),
            location=(
                Location.from_ris_api_dto(body_ris_api_dto.get("location"))
                if body_ris_api_dto.get("location")
                else None
            ),
            keyword=body_ris_api_dto.get("keyword"),
            created=(
                None
                if body_ris_api_dto.get("created") == None
                else datetime.fromisoformat(body_ris_api_dto.get("created"))
            ),
            modified=(
                None
                if body_ris_api_dto.get("modified") == None
                else datetime.fromisoformat(body_ris_api_dto.get("modified"))
            ),
            web=body_ris_api_dto.get("web"),
            deleted=body_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "Body":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            # system=None, # Not stored in DB
            short_name=db_node_dict.get("short_name"),
            name=db_node_dict.get("name"),
            website=db_node_dict.get("website"),
            license=db_node_dict.get("license"),
            license_valid_since=(
                None
                if db_node_dict.get("license_valid_since") == None
                else datetime.fromtimestamp(
                    db_node_dict.get("license_valid_since").to_native().timestamp()
                )
            ),
            oparl_since=(
                None
                if db_node_dict.get("oparl_since") == None
                else datetime.fromtimestamp(
                    db_node_dict.get("oparl_since").to_native().timestamp()
                )
            ),
            ags=db_node_dict.get("ags"),
            rgs=db_node_dict.get("rgs"),
            equivalent=db_node_dict.get("equivalent"),
            contact_email=db_node_dict.get("contact_email"),
            contact_name=db_node_dict.get("contact_name"),
            # organization=None, # Not stored in DB
            # person=None, # Not stored in DB
            # meeting=None, # Not stored in DB
            # paper=None, # Not stored in DB
            # legislative_term=[], # Not stored in DB
            # agenda_item=None, # Not stored in DB
            # consultation=None, # Not stored in DB
            # file=None, # Not stored in DB
            # location_list=None, # Not stored in DB
            # legislative_term_list=None, # Not stored in DB
            # membership=None, # Not stored in DB
            # classification=None, # Not stored in DB
            # location=None, # Not stored in DB
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
            "system": self.system,
            "short_name": self.short_name,
            "name": self.name,
            "website": self.website,
            "license": self.license,
            "license_valid_since": self.license_valid_since,
            "oparl_since": self.oparl_since,
            "ags": self.ags,
            "rgs": self.rgs,
            "equivalent": self.equivalent,
            "contact_email": self.contact_email,
            "contact_name": self.contact_name,
            "organization": self.organization,
            "person": self.person,
            "meeting": self.meeting,
            "paper": self.paper,
            "legislative_term": (
                [term.to_dict() for term in self.legislative_term]
                if self.legislative_term
                else None
            ),
            "agenda_item": self.agenda_item,
            "consultation": self.consultation,
            "file": self.file,
            "location_list": self.location_list,
            "legislative_term_list": self.legislative_term_list,
            "membership": self.membership,
            "classification": self.classification,
            "location": (
                self.location
                if isinstance(self.location, str)
                else self.location.to_dict() if self.location else None
            ),
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
            # "system": self.system,
            "short_name": self.short_name,
            "name": self.name,
            "website": self.website,
            "license": self.license,
            "license_valid_since": self.license_valid_since,
            "oparl_since": self.oparl_since,
            "ags": self.ags,
            "rgs": self.rgs,
            "equivalent": self.equivalent,
            "contact_email": self.contact_email,
            "contact_name": self.contact_name,
            # "organization": self.organization,
            # "person": self.person,
            # "meeting": self.meeting,
            # "paper": self.paper,
            # "legislative_term": self.legislative_term,
            # "agenda_item": self.agenda_item,
            # "consultation": self.consultation,
            # "file": self.file,
            # "location_list": self.location_list,
            # "legislative_term_list": self.legislative_term_list,
            # "membership": self.membership,
            # "classification": self.classification,
            # "location": self.location,
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
            # RetrieverLlmXmlField("system", self.system),
            RetrieverLlmXmlField("short_name", self.short_name),
            RetrieverLlmXmlField("name", self.name),
            # RetrieverLlmXmlField("website", self.website),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("license_valid_since", self.license_valid_since),
            # RetrieverLlmXmlField("oparl_since", self.oparl_since),
            # RetrieverLlmXmlField("ags", self.ags),
            # RetrieverLlmXmlField("rgs", self.rgs),
            # RetrieverLlmXmlField("equivalent", self.equivalent),
            RetrieverLlmXmlField("contact_email", self.contact_email),
            RetrieverLlmXmlField("contact_name", self.contact_name),
            # RetrieverLlmXmlField("organization", self.organization),
            # RetrieverLlmXmlField("person", self.person),
            # RetrieverLlmXmlField("meeting", self.meeting),
            # RetrieverLlmXmlField("paper", self.paper),
            # RetrieverLlmXmlField("legislative_term", self.legislative_term),
            # RetrieverLlmXmlField("agenda_item", self.agenda_item),
            # RetrieverLlmXmlField("consultation", self.consultation),
            # RetrieverLlmXmlField("file", self.file),
            # RetrieverLlmXmlField("location_list", self.location_list),
            # RetrieverLlmXmlField("legislative_term_list", self.legislative_term_list),
            # RetrieverLlmXmlField("membership", self.membership),
            # RetrieverLlmXmlField("classification", self.classification),
            # RetrieverLlmXmlField("location", self.location),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
