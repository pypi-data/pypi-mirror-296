from enum import Enum


class HitStep(Enum):
    INITIAL = "INITIAL"
    RETRIEVED = "RETRIEVED"
    FILE_SECTION_RETRIEVED = "FILE_SECTION_RETRIEVED"
    DOUBLED = "DOUBLED"  # Doubled hits end on this state
    NOT_DOUBLED = "NOT_DOUBLED"
    RELEVANCE_GRADED = "RELEVANCE_GRADED"
    RELATED_DATA_GATHERED = (
        "RELATED_DATA_GATHERED"  # Not doubled hits end on this state
    )
