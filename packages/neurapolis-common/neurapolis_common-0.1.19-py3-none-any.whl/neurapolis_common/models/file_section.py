from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState


class FileSection(BaseModel, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    file_id: Optional[str] = Field(default=None)
    text: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

    @classmethod
    def from_db_node_dict(cls, file_section_db_node_dict: dict) -> "FileSection":
        return cls(
            id=file_section_db_node_dict.get("id"),
            file_id=file_section_db_node_dict.get("file_id"),
            text=file_section_db_node_dict.get("text"),
            created_at=(
                None
                if file_section_db_node_dict.get("created_at") == None
                else datetime.fromtimestamp(
                    file_section_db_node_dict.get("created_at").to_native().timestamp()
                )
            ),
            modified_at=(
                None
                if file_section_db_node_dict.get("modified_at") == None
                else datetime.fromtimestamp(
                    file_section_db_node_dict.get("modified_at").to_native().timestamp()
                )
            ),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "file_id": self.file_id,
            "text": self.text,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }

    def to_db_node_dict(self) -> dict:
        return {
            "id": self.id,
            # "file_id": self.file_id,
            "text": self.text,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }

    def get_llm_xml_fields(self) -> list[RetrieverLlmXmlField]:
        return [
            RetrieverLlmXmlField("id", self.id),
            # RetrieverLlmXmlField("file_id", self.file_id),
            RetrieverLlmXmlField("text", self.text),
            # RetrieverLlmXmlField("created_at", self.created_at),
            # RetrieverLlmXmlField("modified_at", self.modified_at),
        ]
