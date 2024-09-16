from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class System(BaseModel, RisApiDto, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    oparl_version: Optional[str] = Field(default=None)
    other_oparl_versions: Optional[list[str]] = Field(default=None)
    license: Optional[str] = Field(default=None)
    body: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    contact_email: Optional[str] = Field(default=None)
    contact_name: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    vendor: Optional[str] = Field(default=None)
    product: Optional[str] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, system_ris_api_dto: dict) -> "System":
        return cls(
            id=system_ris_api_dto.get("id"),
            type=system_ris_api_dto.get("type"),
            oparl_version=system_ris_api_dto.get("oparlVersion"),
            other_oparl_versions=system_ris_api_dto.get("otherOparlVersions"),
            license=system_ris_api_dto.get("license"),
            body=system_ris_api_dto.get("body"),
            name=system_ris_api_dto.get("name"),
            contact_email=system_ris_api_dto.get("contactEmail"),
            contact_name=system_ris_api_dto.get("contactName"),
            website=system_ris_api_dto.get("website"),
            vendor=system_ris_api_dto.get("vendor"),
            product=system_ris_api_dto.get("product"),
            created=(
                None
                if system_ris_api_dto.get("created") == None
                else datetime.strptime(
                    system_ris_api_dto.get("created"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            modified=(
                None
                if system_ris_api_dto.get("modified") == None
                else datetime.strptime(
                    system_ris_api_dto.get("modified"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            web=system_ris_api_dto.get("web"),
            deleted=system_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "System":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            oparl_version=db_node_dict.get("oparl_version"),
            other_oparl_versions=db_node_dict.get("other_oparl_versions"),
            license=db_node_dict.get("license"),
            # body=None, # Not stored in DB
            name=db_node_dict.get("name"),
            contact_email=db_node_dict.get("contact_email"),
            contact_name=db_node_dict.get("contact_name"),
            website=db_node_dict.get("website"),
            vendor=db_node_dict.get("vendor"),
            product=db_node_dict.get("product"),
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
            "oparl_version": self.oparl_version,
            "other_oparl_versions": self.other_oparl_versions,
            "license": self.license,
            "body": self.body,
            "name": self.name,
            "contact_email": self.contact_email,
            "contact_name": self.contact_name,
            "website": self.website,
            "vendor": self.vendor,
            "product": self.product,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }

    def to_db_node_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "oparl_version": self.oparl_version,
            "other_oparl_versions": self.other_oparl_versions,
            "license": self.license,
            # "body": self.body,
            "name": self.name,
            "contact_email": self.contact_email,
            "contact_name": self.contact_name,
            "website": self.website,
            "vendor": self.vendor,
            "product": self.product,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }

    def get_llm_xml_fields(self) -> list[RetrieverLlmXmlField]:
        return [
            RetrieverLlmXmlField("id", self.id),
            # RetrieverLlmXmlField("type", self.type),
            # RetrieverLlmXmlField("oparl_version", self.oparl_version),
            # RetrieverLlmXmlField("other_oparl_versions", self.other_oparl_versions),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("body", self.body),
            RetrieverLlmXmlField("name", self.name),
            # RetrieverLlmXmlField("contact_email", self.contact_email),
            # RetrieverLlmXmlField("contact_name", self.contact_name),
            # RetrieverLlmXmlField("website", self.website),
            # RetrieverLlmXmlField("vendor", self.vendor),
            # RetrieverLlmXmlField("product", self.product),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
