from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .file import File
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class AgendaItem(
    BaseModel,
    RisApiDto,
    DbNodeDict,
    RetrieverState,
):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    meeting: Optional[str] = Field(default=None)
    number: Optional[str] = Field(default=None)
    order: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    public: Optional[bool] = Field(default=None)
    consultation: Optional[str] = Field(default=None)
    result: Optional[str] = Field(default=None)
    resolution_text: Optional[str] = Field(default=None)
    resolution_file: Optional[File] = Field(default=None)
    auxiliary_file: Optional[list[File]] = Field(default=None)
    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)
    license: Optional[str] = Field(default=None)
    keyword: Optional[list[str]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, agenda_item_ris_api_dto: dict) -> "AgendaItem":
        return cls(
            id=agenda_item_ris_api_dto.get("id"),
            type=agenda_item_ris_api_dto.get("type"),
            meeting=agenda_item_ris_api_dto.get("meeting"),
            number=agenda_item_ris_api_dto.get("number"),
            order=agenda_item_ris_api_dto.get("order"),
            name=agenda_item_ris_api_dto.get("name"),
            public=agenda_item_ris_api_dto.get("public"),
            consultation=agenda_item_ris_api_dto.get("consultation"),
            result=agenda_item_ris_api_dto.get("result"),
            resolution_text=agenda_item_ris_api_dto.get("resolutionText"),
            resolution_file=(
                File.from_ris_api_dto(agenda_item_ris_api_dto.get("resolutionFile"))
                if agenda_item_ris_api_dto.get("resolutionFile")
                else None
            ),
            auxiliary_file=(
                [
                    File.from_ris_api_dto(x_auxiliary_file_ris_api_dto)
                    for x_auxiliary_file_ris_api_dto in agenda_item_ris_api_dto.get(
                        "auxiliaryFile"
                    )
                ]
                if agenda_item_ris_api_dto.get("auxiliaryFile")
                else None
            ),
            start=(
                None
                if agenda_item_ris_api_dto.get("start") == None
                else datetime.strptime(
                    agenda_item_ris_api_dto.get("start"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            end=(
                None
                if agenda_item_ris_api_dto.get("end") == None
                else datetime.strptime(
                    agenda_item_ris_api_dto.get("end"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            license=agenda_item_ris_api_dto.get("license"),
            keyword=agenda_item_ris_api_dto.get("keyword"),
            created=(
                None
                if agenda_item_ris_api_dto.get("created") == None
                else datetime.strptime(
                    agenda_item_ris_api_dto.get("created"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            modified=(
                None
                if agenda_item_ris_api_dto.get("modified") == None
                else datetime.strptime(
                    agenda_item_ris_api_dto.get("modified"), "%Y-%m-%dT%H:%M:%S%z"
                )
            ),
            web=agenda_item_ris_api_dto.get("web"),
            deleted=agenda_item_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "AgendaItem":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            meeting=None,  # Not stored in DB
            number=db_node_dict.get("number"),
            order=db_node_dict.get("order"),
            name=db_node_dict.get("name"),
            public=db_node_dict.get("public"),
            consultation=None,  # Not stored in DB
            result=db_node_dict.get("result"),
            resolution_text=db_node_dict.get("resolution_text"),
            resolution_file=None,  # Not stored in DB
            auxiliary_file=None,  # Not stored in DB
            start=(
                None
                if db_node_dict.get("start") == None
                else datetime.fromtimestamp(
                    db_node_dict.get("start").to_native().timestamp()
                )
            ),
            end=(
                None
                if db_node_dict.get("end") == None
                else datetime.fromtimestamp(
                    db_node_dict.get("end").to_native().timestamp()
                )
            ),
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
            "meeting": self.meeting,
            "number": self.number,
            "order": self.order,
            "name": self.name,
            "public": self.public,
            "consultation": self.consultation,
            "result": self.result,
            "resolution_text": self.resolution_text,
            "resolution_file": (
                self.resolution_file.to_dict() if self.resolution_file else None
            ),
            "auxiliary_file": (
                [file.to_dict() for file in self.auxiliary_file]
                if self.auxiliary_file
                else None
            ),
            "start": self.start,
            "end": self.end,
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
            # "meeting": self.meeting,
            "number": self.number,
            "order": self.order,
            "name": self.name,
            "public": self.public,
            # "consultation": self.consultation,
            "result": self.result,
            "resolution_text": self.resolution_text,
            # "resolution_file": self.resolution_file,
            # "auxiliary_file": self.auxiliary_file,
            "start": self.start,
            "end": self.end,
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
            RetrieverLlmXmlField("type", self.type),
            # RetrieverLlmXmlField("meeting", self.meeting),
            RetrieverLlmXmlField("number", self.number),
            # RetrieverLlmXmlField("order", self.order),
            RetrieverLlmXmlField("name", self.name),
            RetrieverLlmXmlField("public", self.public),
            # RetrieverLlmXmlField("consultation", self.consultation),
            RetrieverLlmXmlField("result", self.result),
            RetrieverLlmXmlField("resolution_text", self.resolution_text),
            # RetrieverLlmXmlField("resolution_file", self.resolution_file),
            # RetrieverLlmXmlField("auxiliary_file", self.auxiliary_file),
            RetrieverLlmXmlField("start", self.start),
            RetrieverLlmXmlField("end", self.end),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
