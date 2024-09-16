import uuid
from typing import Optional

from neurapolis_common.models.agenda_item import AgendaItem
from neurapolis_common.models.consultation import Consultation
from neurapolis_common.models.file import File
from neurapolis_common.models.file_chunk import FileChunk
from neurapolis_common.models.file_section import FileSection
from neurapolis_common.models.meeting import Meeting
from neurapolis_common.models.organization import Organization
from neurapolis_common.models.paper import Paper
from neurapolis_common.models.person import Person

# from neurapolis_common.models.retriever_state import RetrieverState
from pydantic import BaseModel, Field

from neurapolis_retriever.state.grading import Grading
from neurapolis_retriever.state.hit_step import HitStep


class Hit(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    step: HitStep = Field()
    file_chunk: FileChunk = Field()
    file_section: Optional[FileSection] = Field(default=None)
    doubled_hit_id: Optional[str] = Field(default=None)
    grading: Optional[Grading] = Field(default=None)
    related_file: Optional[File] = Field(default=None)
    related_meeting: Optional[Meeting] = Field(default=None)
    related_paper: Optional[Paper] = Field(default=None)
    related_consultation: Optional[Consultation] = Field(default=None)
    related_agenda_item: Optional[AgendaItem] = Field(default=None)
    related_persons: Optional[list[Person]] = Field(default=None)
    related_organizations: Optional[list[Organization]] = Field(default=None)

    def format_to_text(self) -> str:
        return self.file_section.text

    @staticmethod
    def format_hit_to_inner_xml(hit: "Hit") -> str:
        return f"<Treffer>\n{hit.format_to_text()}\n</Treffer>"
