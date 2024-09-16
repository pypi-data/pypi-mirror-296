from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .consultation import Consultation
from .db_node_dict import DbNodeDict
from .file import File
from .location import Location
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState
from .ris_api_dto import RisApiDto


class Paper(BaseModel, RisApiDto, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    body: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    reference: Optional[str] = Field(default=None)
    date: Optional[datetime] = Field(default=None)
    paper_type: Optional[str] = Field(default=None)
    related_paper: Optional[list[str]] = Field(default=None)
    superordinated_paper: Optional[list[str]] = Field(default=None)
    subordinated_paper: Optional[list[str]] = Field(default=None)
    main_file: Optional[File] = Field(default=None)
    auxiliary_file: Optional[list[File]] = Field(default=None)
    location: Optional[list[Location]] = Field(default=None)
    originator_person: Optional[list[str]] = Field(default=None)
    under_direction_of: Optional[list[str]] = Field(default=None)
    originator_organization: Optional[list[str]] = Field(default=None)
    consultation: Optional[list[Consultation]] = Field(default=None)
    license: Optional[str] = Field(default=None)
    keyword: Optional[list[str]] = Field(default=None)
    created: Optional[datetime] = Field(default=None)
    modified: Optional[datetime] = Field(default=None)
    web: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)

    @classmethod
    def from_ris_api_dto(cls, paper_ris_api_dto: dict) -> "Paper":
        return cls(
            id=paper_ris_api_dto.get("id"),
            type=paper_ris_api_dto.get("type"),
            body=paper_ris_api_dto.get("body"),
            name=paper_ris_api_dto.get("name"),
            reference=paper_ris_api_dto.get("reference"),
            date=(
                None
                if paper_ris_api_dto.get("date") == None
                else datetime.fromisoformat(paper_ris_api_dto.get("date"))
            ),
            paper_type=paper_ris_api_dto.get("paperType"),
            related_paper=paper_ris_api_dto.get("relatedPaper"),
            superordinated_paper=paper_ris_api_dto.get("superordinatedPaper"),
            subordinated_paper=paper_ris_api_dto.get("subordinatedPaper"),
            main_file=(
                File.from_ris_api_dto(paper_ris_api_dto.get("mainFile"))
                if paper_ris_api_dto.get("mainFile")
                else None
            ),
            auxiliary_file=(
                [
                    File.from_ris_api_dto(x_file_ris_api_dto)
                    for x_file_ris_api_dto in paper_ris_api_dto.get("auxiliaryFile")
                ]
                if paper_ris_api_dto.get("auxiliaryFile")
                else None
            ),
            location=(
                [
                    Location.from_ris_api_dto(x_location_ris_api_dto)
                    for x_location_ris_api_dto in paper_ris_api_dto.get("location")
                ]
                if paper_ris_api_dto.get("location")
                else None
            ),
            originator_person=paper_ris_api_dto.get("originatorPerson"),
            under_direction_of=paper_ris_api_dto.get("underDirectionOf"),
            originator_organization=paper_ris_api_dto.get("originatorOrganization"),
            consultation=(
                [
                    Consultation.from_ris_api_dto(x_consultation_ris_api_dto)
                    for x_consultation_ris_api_dto in paper_ris_api_dto.get(
                        "consultation", []
                    )
                ]
                if paper_ris_api_dto.get("consultation")
                else None
            ),
            license=paper_ris_api_dto.get("license"),
            keyword=paper_ris_api_dto.get("keyword"),
            created=(
                datetime.strptime(
                    paper_ris_api_dto.get("created"), "%Y-%m-%dT%H:%M:%S%z"
                )
                if paper_ris_api_dto.get("created")
                else None
            ),
            modified=(
                datetime.strptime(
                    paper_ris_api_dto.get("modified"), "%Y-%m-%dT%H:%M:%S%z"
                )
                if paper_ris_api_dto.get("modified")
                else None
            ),
            web=paper_ris_api_dto.get("web"),
            deleted=paper_ris_api_dto.get("deleted"),
        )

    @classmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> "Paper":
        return cls(
            id=db_node_dict.get("id"),
            type=db_node_dict.get("type"),
            # body=None,  # Not stored in DB
            name=db_node_dict.get("name"),
            reference=db_node_dict.get("reference"),
            date=(
                None
                if db_node_dict.get("date") == None
                else datetime.fromtimestamp(
                    db_node_dict.get("date").to_native().timestamp()
                )
            ),
            paper_type=db_node_dict.get("paper_type"),
            # related_paper=None,  # Not stored in DB
            # superordinated_paper=None,  # Not stored in DB
            # subordinated_paper=None,  # Not stored in DB
            # main_file=None,  # Not stored in DB
            # auxiliary_file=None,  # Not stored in DB
            # location=None,  # Not stored in DB
            # originator_person=None,  # Not stored in DB
            # under_direction_of=None,  # Not stored in DB
            # originator_organization=None,  # Not stored in DB
            # consultation=None,  # Not stored in DB
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
            "reference": self.reference,
            "date": self.date,
            "paper_type": self.paper_type,
            "related_paper": self.related_paper,
            "superordinated_paper": self.superordinated_paper,
            "subordinated_paper": self.subordinated_paper,
            "main_file": self.main_file.to_dict() if self.main_file else None,
            "auxiliary_file": (
                [file.to_dict() for file in self.auxiliary_file]
                if self.auxiliary_file
                else None
            ),
            "location": (
                [loc.to_dict() for loc in self.location] if self.location else None
            ),
            "originator_person": self.originator_person,
            "under_direction_of": self.under_direction_of,
            "originator_organization": self.originator_organization,
            "consultation": (
                [cons.to_dict() for cons in self.consultation]
                if self.consultation
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
            # "body": self.body,
            "name": self.name,
            "reference": self.reference,
            "date": self.date,
            "paper_type": self.paper_type,
            # "related_paper": self.related_paper,
            # "superordinated_paper": self.superordinated_paper,
            # "subordinated_paper": self.subordinated_paper,
            # "main_file": self.main_file,
            # "auxiliary_file": self.auxiliary_file,
            # "location": self.location,
            # "originator_person": self.originator_person,
            # "under_direction_of": self.under_direction_of,
            # "originator_organization": self.originator_organization,
            # "consultation": self.consultation,
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
            RetrieverLlmXmlField("body", self.body),
            RetrieverLlmXmlField("name", self.name),
            RetrieverLlmXmlField("reference", self.reference),
            RetrieverLlmXmlField("date", self.date),
            RetrieverLlmXmlField("paper_type", self.paper_type),
            # RetrieverLlmXmlField("related_paper", self.related_paper),
            # RetrieverLlmXmlField("superordinated_paper", self.superordinated_paper),
            # RetrieverLlmXmlField("subordinated_paper", self.subordinated_paper),
            # RetrieverLlmXmlField("main_file", self.main_file),
            # RetrieverLlmXmlField("auxiliary_file", self.auxiliary_file),
            # RetrieverLlmXmlField("location", self.location),
            # RetrieverLlmXmlField("originator_person", self.originator_person),
            # RetrieverLlmXmlField("under_direction_of", self.under_direction_of),
            # RetrieverLlmXmlField("originator_organization", self.originator_organization),
            # RetrieverLlmXmlField("consultation", self.consultation),
            # RetrieverLlmXmlField("license", self.license),
            # RetrieverLlmXmlField("keyword", self.keyword),
            # RetrieverLlmXmlField("created", self.created),
            # RetrieverLlmXmlField("modified", self.modified),
            # RetrieverLlmXmlField("web", self.web),
            # RetrieverLlmXmlField("deleted", self.deleted),
        ]
