from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .db_node_dict import DbNodeDict
from .retriever_llm_xml_field import RetrieverLlmXmlField
from .retriever_state import RetrieverState


class FileChunk(BaseModel, DbNodeDict, RetrieverState):
    id: Optional[str] = Field(default=None)
    file_section_id: Optional[str] = Field(default=None)
    text: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    modified_at: Optional[datetime] = Field(default=None)

    @classmethod
    def from_db_node_dict(cls, file_db_node_dict: dict) -> "FileChunk":
        created_at = file_db_node_dict.get("created_at")
        modified_at = file_db_node_dict.get("modified_at")
        return cls(
            id=file_db_node_dict.get("id"),
            file_section_id=file_db_node_dict.get("file_section_id"),
            text=file_db_node_dict.get("text"),
            created_at=(
                datetime.fromtimestamp(created_at.to_native().timestamp())
                if created_at
                else None
            ),
            modified_at=(
                datetime.fromtimestamp(modified_at.to_native().timestamp())
                if modified_at
                else None
            ),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "file_section_id": self.file_section_id,
            "text": self.text,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }

    def to_db_node_dict(self) -> dict:
        return {
            "id": self.id,
            # "file_section_id": self.file_section_id,
            "text": self.text,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }

    def get_llm_xml_fields(self) -> list[RetrieverLlmXmlField]:
        return [
            RetrieverLlmXmlField("id", self.id),
            # RetrieverLlmXmlField("file_section_id", self.file_section_id),
            RetrieverLlmXmlField("text", self.text),
            # RetrieverLlmXmlField("created_at", self.created_at),
            # RetrieverLlmXmlField("modified_at", self.modified_at),
        ]
