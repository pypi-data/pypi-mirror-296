from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .agenda_item import AgendaItem
from .db_node_dict import DbNodeDict
from .file import File
from .location import Location
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class Meeting(BaseModel, RisApiDto, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    meeting_state: Optional[str] = Field(default=None)
    cancelled: Optional[bool] = Field(default=None)
    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)
    location: Optional[Location] = Field(default=None)
    organization: Optional[list[str]] = Field(default=None)
    participant: Optional[list[str]] = Field(default=None)
    invitation: Optional[File] = Field(default=None)
    results_protocol: Optional[File] = Field(default=None)
    verbatim_protocol: Optional[File] = Field(default=None)
    auxiliary_file: Optional[list[File]] = Field(default=None)
    agenda_item: Optional[list[AgendaItem]] = Field(default=None)
    license: Optional[str] = Field(default=None)
    keyword: Optional[list[str]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, meeting_ris_api_dto: dict) -> "Meeting":
        return cls(
            id=meeting_ris_api_dto.get("id"),
            type=meeting_ris_api_dto.get("type"),
            name=meeting_ris_api_dto.get("name"),
            meeting_state=meeting_ris_api_dto.get("meetingState"),
            cancelled=meeting_ris_api_dto.get("cancelled"),
            start=(
                None
                if meeting_ris_api_dto.get("start") == None
                else datetime.fromisoformat(meeting_ris_api_dto.get("start"))
            ),
            end=(
                None
                if meeting_ris_api_dto.get("end") == None
                else datetime.fromisoformat(meeting_ris_api_dto.get("end"))
            ),
            location=(
                Location.from_ris_api_dto(meeting_ris_api_dto.get("location"))
                if meeting_ris_api_dto.get("location")
                else None
            ),
            organization=meeting_ris_api_dto.get("organization"),
            participant=meeting_ris_api_dto.get("participant"),
            invitation=(
                File.from_ris_api_dto(meeting_ris_api_dto.get("invitation"))
                if meeting_ris_api_dto.get("invitation")
                else None
            ),
            results_protocol=(
                File.from_ris_api_dto(meeting_ris_api_dto.get("resultsProtocol"))
                if meeting_ris_api_dto.get("resultsProtocol")
                else None
            ),
            verbatim_protocol=(
                File.from_ris_api_dto(meeting_ris_api_dto.get("verbatimProtocol"))
                if meeting_ris_api_dto.get("verbatimProtocol")
                else None
            ),
            auxiliary_file=(
                [
                    File.from_ris_api_dto(x_file_ris_api_dto)
                    for x_file_ris_api_dto in meeting_ris_api_dto.get("auxiliaryFile")
                ]
                if meeting_ris_api_dto.get("auxiliaryFile")
                else None
            ),
            agenda_item=(
                [
                    AgendaItem.from_ris_api_dto(x_agenda_item_ris_api_dto)
                    for x_agenda_item_ris_api_dto in meeting_ris_api_dto.get(
                        "agendaItem"
                    )
                ]
                if meeting_ris_api_dto.get("agendaItem")
                else None
            ),
            license=meeting_ris_api_dto.get("license"),
            keyword=meeting_ris_api_dto.get("keyword"),
            created=(
                datetime.strptime(
                    meeting_ris_api_dto.get("created"), "%Y-%m-%dT%H:%M:%S%z"
                )
                if meeting_ris_api_dto.get("created")
                else None
            ),
            modified=(
                datetime.strptime(
                    meeting_ris_api_dto.get("modified"), "%Y-%m-%dT%H:%M:%S%z"
                )
                if meeting_ris_api_dto.get("modified")
                else None
            ),
            web=meeting_ris_api_dto.get("web"),
            deleted=meeting_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "Meeting":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            name=db_node_dict.get("name"),
            meeting_state=db_node_dict.get("meeting_state"),
            cancelled=db_node_dict.get("cancelled"),
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
            # location=None,  # Not stored in DB
            # organization=None,  # Not stored in DB
            # participant=None,  # Not stored in DB
            # invitation=None,  # Not stored in DB
            # results_protocol=None,  # Not stored in DB
            # verbatim_protocol=None,  # Not stored in DB
            # auxiliary_file=None,  # Not stored in DB
            # agenda_item=None,  # Not stored in DB
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
            "name": self.name,
            "meeting_state": self.meeting_state,
            "cancelled": self.cancelled,
            "start": self.start,
            "end": self.end,
            "location": self.location.to_dict() if self.location else None,
            "organization": self.organization,
            "participant": self.participant,
            "invitation": self.invitation.to_dict() if self.invitation else None,
            "results_protocol": (
                self.results_protocol.to_dict() if self.results_protocol else None
            ),
            "verbatim_protocol": (
                self.verbatim_protocol.to_dict() if self.verbatim_protocol else None
            ),
            "auxiliary_file": (
                [x_file.to_dict() for x_file in self.auxiliary_file]
                if self.auxiliary_file
                else None
            ),
            "agenda_item": (
                [x_agenda_item.to_dict() for x_agenda_item in self.agenda_item]
                if self.agenda_item
                else None
            ),
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
            "name": self.name,
            "meeting_state": self.meeting_state,
            "cancelled": self.cancelled,
            "start": self.start,
            "end": self.end,
            # "location": self.location,
            # "organization": self.organization,
            # "participant": self.participant,
            # "invitation": self.invitation,
            # "results_protocol": self.results_protocol,
            # "verbatim_protocol": self.verbatim_protocol,
            # "auxiliary_file": self.auxiliary_file,
            # "agenda_item": self.agenda_item,
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
            RetrieverLlmXmlField("name", self.name),
            RetrieverLlmXmlField("meeting_state", self.meeting_state),
            RetrieverLlmXmlField("cancelled", self.cancelled),
            RetrieverLlmXmlField("start", self.start),
            RetrieverLlmXmlField("end", self.end),
            # RetrieverLlmXmlField("location", self.location),
            # RetrieverLlmXmlField("organization", self.organization),
            # RetrieverLlmXmlField("participant", self.participant),
            # RetrieverLlmXmlField("invitation", self.invitation),
            # RetrieverLlmXmlField("results_protocol", self.results_protocol),
            # RetrieverLlmXmlField("verbatim_protocol", self.verbatim_protocol),
            # RetrieverLlmXmlField("auxiliary_file", self.auxiliary_file),
            # RetrieverLlmXmlField("agenda_item", self.agenda_item),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
