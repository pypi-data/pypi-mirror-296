from pydantic import BaseModel, Field


class Grading(BaseModel):
    is_relevant: bool = Field()
    feedback: str = Field()
