from dataclasses import dataclass


@dataclass
class Theme:
    id: int
    title: str


@dataclass
class Answer:
    title: str
    is_correct: bool


@dataclass
class Question:
    id: int
    title: str
    theme_id: int
    answers: list[Answer]
