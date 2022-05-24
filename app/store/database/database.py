from dataclasses import dataclass, field

from app.quiz.models import Theme, Question
from app.admin.models import Admin


@dataclass
class Database:
    # TODO: добавить поля admins и questions
    admins: list[Admin] = field(default_factory=list)
    themes: list[Theme] = field(default_factory=list)
    questions: list[Question] = field(default_factory=list)

    @property
    def next_theme_id(self) -> int:
        return len(self.themes) + 1

    @property
    def next_admin_id(self) -> int:
        return len(self.admins) + 1

    @property
    def next_question_id(self) -> int:
        return len(self.questions) + 1

    def clear(self):
        self.admins = []
        self.themes = []
        self.questions = []
