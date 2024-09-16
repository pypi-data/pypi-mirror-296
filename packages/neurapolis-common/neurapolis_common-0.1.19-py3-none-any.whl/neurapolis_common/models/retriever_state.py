from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from .retriever_llm_xml_field import RetrieverLlmXmlField

T = TypeVar("T", bound="RetrieverState")


class RetrieverState(ABC):
    @abstractmethod
    def get_llm_xml_fields(self) -> list[RetrieverLlmXmlField]:
        pass

    def format_to_llm_xml(self, xml_tag_name: str) -> str:
        fields = self.get_llm_xml_fields()
        inner_xml_lines = []
        for field in fields:
            if field.value == None:
                continue
            inner_xml_lines.append(f"<{field.name}>{field.value}</{field.name}>")
        inner_xml = "".join(inner_xml_lines)
        return f"<{xml_tag_name}>{inner_xml}</{xml_tag_name}>"
