import re
import uuid

from pydantic import Field, create_model


def generate_grading_llm_data_model() -> type:
    fields = {
        "is_hit_relevant": (
            bool,
            Field(description="Is the hit relevant?"),
        ),
        "hit_feedback": (
            str,
            Field(
                description="Very short feedback on why the hit is relevant or not.",
            ),
        ),
    }
    model_name = "GradingLlmDataModel" + re.sub("[^a-zA-Z]", "", str(uuid.uuid4()))
    return create_model(model_name, **fields)
