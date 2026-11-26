from typing import Any

import pytest
from pydantic import ValidationError

from app.generation.schemas import GeneratedQuestion, QuestionBatch


def make_question(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "question_type": "mcq",
        "difficulty": "easy",
        "text": "What is the capital of Egypt?",
        "options": ["Cairo", "Alexandria", "Luxor", "Aswan"],
        "correct_option_index": 0,
        "explanation": "Cairo is the capital.",
        "source_quote": "Cairo is the capital of Egypt.",
    }
    data.update(overrides)
    return data


def test_valid_mcq_is_accepted() -> None:
    question = GeneratedQuestion(**make_question())
    assert question.options[question.correct_option_index] == "Cairo"


def test_valid_true_false_is_accepted() -> None:
    question = GeneratedQuestion(
        **make_question(
            question_type="true_false",
            options=["صح", "غلط"],
            correct_option_index=1,
        )
    )
    assert len(question.options) == 2


def test_options_are_stripped() -> None:
    question = GeneratedQuestion(
        **make_question(options=["  Cairo ", "Giza", "Luxor", "Aswan"])
    )
    assert question.options[0] == "Cairo"


@pytest.mark.parametrize(
    "overrides",
    [
        {"options": ["Cairo", "Giza"]},
        {"options": ["Cairo"] * 4},
        {"options": ["Cairo", "Giza", "Luxor", " "]},
        {"correct_option_index": 4},
        {"correct_option_index": -1},
        {"question_type": "true_false"},
        {"difficulty": "extreme"},
        {"source_quote": ""},
    ],
)
def test_invalid_questions_are_rejected(overrides: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        GeneratedQuestion(**make_question(**overrides))


def test_batch_parses_list_of_questions() -> None:
    batch = QuestionBatch(questions=[make_question(), make_question()])
    assert len(batch.questions) == 2
