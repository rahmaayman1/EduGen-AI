from enum import Enum

from pydantic import BaseModel, Field, model_validator

MCQ_MIN_OPTIONS = 3
MCQ_MAX_OPTIONS = 5
TRUE_FALSE_OPTION_COUNT = 2


class QuestionType(str, Enum):
    MCQ = "mcq"
    TRUE_FALSE = "true_false"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GeneratedQuestion(BaseModel):
    """A single question produced by the LLM, validated for structure only."""

    question_type: QuestionType
    difficulty: Difficulty
    text: str = Field(min_length=5)
    options: list[str]
    correct_option_index: int = Field(ge=0)
    explanation: str = Field(min_length=1)
    source_quote: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_options(self) -> "GeneratedQuestion":
        self.options = [option.strip() for option in self.options]

        if any(not option for option in self.options):
            raise ValueError("options must not contain empty values")

        lowered = [option.lower() for option in self.options]
        if len(set(lowered)) != len(lowered):
            raise ValueError("options must be unique")

        if self.question_type == QuestionType.TRUE_FALSE:
            if len(self.options) != TRUE_FALSE_OPTION_COUNT:
                raise ValueError("true_false questions need exactly 2 options")
        elif not MCQ_MIN_OPTIONS <= len(self.options) <= MCQ_MAX_OPTIONS:
            raise ValueError(
                f"mcq questions need {MCQ_MIN_OPTIONS}-{MCQ_MAX_OPTIONS} options"
            )

        if self.correct_option_index >= len(self.options):
            raise ValueError("correct_option_index is out of range")

        return self


class QuestionBatch(BaseModel):
    """The structured response expected from one generation call."""

    questions: list[GeneratedQuestion]
