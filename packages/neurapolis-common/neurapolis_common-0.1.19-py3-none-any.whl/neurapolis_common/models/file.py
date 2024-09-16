from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class File(BaseModel, RisApiDto, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    file_name: Optional[str] = Field(default=None)
    mime_type: Optional[str] = Field(default=None)
    date: Optional[datetime] = Field(default=None)
    size: Optional[int] = Field(default=None)
    sha1_checksum: Optional[str] = Field(default=None)
    sha512_checksum: Optional[str] = Field(default=None)
    text: Optional[str] = Field(default=None)
    access_url: Optional[str] = Field(default=None)
    download_url: Optional[str] = Field(default=None)
    external_service_url: Optional[str] = Field(default=None)
    master_file: Optional[str] = Field(default=None)
    derivative_file: Optional[list[str]] = Field(default=None)
    file_license: Optional[str] = Field(default=None)
    meeting: Optional[list[str]] = Field(default=None)
    agenda_item: Optional[list[str]] = Field(default=None)
    paper: Optional[list[str]] = Field(default=None)
    license: Optional[str] = Field(default=None)
    keyword: Optional[list[str]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)
    extracted_text: Optional[str] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, file_ris_api_dto: dict) -> "File":
        return cls(
            id=file_ris_api_dto.get("id"),
            type=file_ris_api_dto.get("type"),
            name=file_ris_api_dto.get("name"),
            file_name=file_ris_api_dto.get("fileName"),
            mime_type=file_ris_api_dto.get("mimeType"),
            date=(
                None
                if file_ris_api_dto.get("date") == None
                else datetime.strptime(
                    file_ris_api_dto.get("date"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            size=file_ris_api_dto.get("size"),
            sha1_checksum=file_ris_api_dto.get("sha1Checksum"),
            sha512_checksum=file_ris_api_dto.get("sha512Checksum"),
            text=file_ris_api_dto.get("text"),
            access_url=file_ris_api_dto.get("accessUrl"),
            download_url=file_ris_api_dto.get("downloadUrl"),
            external_service_url=file_ris_api_dto.get("externalServiceUrl"),
            master_file=file_ris_api_dto.get("masterFile"),
            derivative_file=file_ris_api_dto.get("derivativeFile"),
            file_license=file_ris_api_dto.get("fileLicense"),
            meeting=file_ris_api_dto.get("meeting"),
            agenda_item=file_ris_api_dto.get("agendaItem"),
            paper=file_ris_api_dto.get("paper"),
            license=file_ris_api_dto.get("license"),
            keyword=file_ris_api_dto.get("keyword"),
            created=(
                None
                if file_ris_api_dto.get("created") == None
                else datetime.strptime(
                    file_ris_api_dto.get("created"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            modified=(
                None
                if file_ris_api_dto.get("modified") == None
                else datetime.strptime(
                    file_ris_api_dto.get("modified"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            web=file_ris_api_dto.get("web"),
            deleted=file_ris_api_dto.get("deleted"),
            extracted_text=file_ris_api_dto.get("extractedText"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "File":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            name=db_node_dict.get("name"),
            file_name=db_node_dict.get("file_name"),
            mime_type=db_node_dict.get("mime_type"),
            date=(
                None
                if db_node_dict.get("date") == None
                else datetime.fromtimestamp(
                    db_node_dict.get("date").to_native().timestamp()
                )
            ),
            size=db_node_dict.get("size"),
            sha1_checksum=db_node_dict.get("sha1_checksum"),
            sha512_checksum=db_node_dict.get("sha512_checksum"),
            text=db_node_dict.get("text"),
            access_url=db_node_dict.get("access_url"),
            download_url=db_node_dict.get("download_url"),
            external_service_url=db_node_dict.get("external_service_url"),
            # master_file=None,  # Not stored in DB
            # derivative_file=None,  # Not stored in DB
            file_license=db_node_dict.get("file_license"),
            # meeting=None,  # Not stored in DB
            # agenda_item=None,  # Not stored in DB
            # paper=None,  # Not stored in DB
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
            extracted_text=db_node_dict.get("extracted_text"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "file_name": self.file_name,
            "mime_type": self.mime_type,
            "date": self.date,
            "size": self.size,
            "sha1_checksum": self.sha1_checksum,
            "sha512_checksum": self.sha512_checksum,
            "text": self.text,
            "access_url": self.access_url,
            "download_url": self.download_url,
            "external_service_url": self.external_service_url,
            "master_file": (
                self.master_file
                if isinstance(self.master_file, str)
                else self.master_file.to_dict() if self.master_file else None
            ),
            "derivative_file": (
                [
                    x_file if isinstance(x_file, str) else x_file.to_dict()
                    for x_file in self.derivative_file
                ]
                if self.derivative_file
                else None
            ),
            "file_license": self.file_license,
            "meeting": self.meeting,
            "agenda_item": self.agenda_item,
            "paper": self.paper,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
            "extracted_text": self.extracted_text,
        }

    def to_db_node_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "file_name": self.file_name,
            "mime_type": self.mime_type,
            "date": self.date,
            "size": self.size,
            "sha1_checksum": self.sha1_checksum,
            "sha512_checksum": self.sha512_checksum,
            "text": self.text,
            "access_url": self.access_url,
            "download_url": self.download_url,
            "external_service_url": self.external_service_url,
            # "master_file": self.master_file,
            # "derivative_file": self.derivative_file,
            "file_license": self.file_license,
            # "meeting": self.meeting,
            # "agenda_item": self.agenda_item,
            # "paper": self.paper,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
            "extracted_text": self.extracted_text,
        }

    def get_llm_xml_fields(self) -> list[RetrieverLlmXmlField]:
        return [
            RetrieverLlmXmlField("id", self.id),
            # RetrieverLlmXmlField("type", self.type),
            RetrieverLlmXmlField("name", self.name),
            RetrieverLlmXmlField("file_name", self.file_name),
            RetrieverLlmXmlField("mime_type", self.mime_type),
            # RetrieverLlmXmlField("date", self.date),
            # RetrieverLlmXmlField("size", self.size),
            # RetrieverLlmXmlField("sha1_checksum", self.sha1_checksum),
            # RetrieverLlmXmlField("sha512_checksum", self.sha512_checksum),
            # RetrieverLlmXmlField("text", self.text),
            RetrieverLlmXmlField("access_url", self.access_url),
            RetrieverLlmXmlField("download_url", self.download_url),
            # RetrieverLlmXmlField("external_service_url", self.external_service_url),
            # RetrieverLlmXmlField("file_license", self.file_license),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
            # RetrieverLlmXmlField("extracted_text", self.extracted_text),
        ]
