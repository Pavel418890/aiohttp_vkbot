import copy
from typing import Optional

from aiohttp.web import HTTPConflict
from aiohttp.web_exceptions import HTTPNotFound, HTTPBadRequest

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Theme, Question, Answer


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        if await self.get_theme_by_title(title):
            raise HTTPConflict
        else:
            theme = Theme(id=self.app.database.next_theme_id, title=str(title))
            self.app.database.themes.append(theme)
            return theme

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        for theme in self.app.database.themes:
            if theme.title == title:
                return theme
        return None

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        themes = self.app.database.themes
        if id_ > len(themes):
            raise HTTPNotFound
        elif id_ < 0:
            raise HTTPBadRequest
        else:
            return themes[id_ - 1]

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        questions = self.app.database.questions
        for question in questions:
            if question.title == title:
                return question
        return None

    async def create_question(
            self, title: str, theme_id: int, answers: list[dict[str, str | bool]]
    ) -> Question:
        theme = await self.get_theme_by_id(theme_id)
        parsed_answers = [Answer(**answer) for answer in answers]
        only_one_correct = 0
        for answer in parsed_answers:
            if answer.is_correct:
                only_one_correct += 1
        if only_one_correct != 1 and len(parsed_answers) < 2:
            raise HTTPBadRequest
        elif await self.get_question_by_title(title):
            raise HTTPConflict
        elif not theme:
            raise HTTPNotFound
        else:
            question = Question(
                title=title,
                theme_id=theme_id,
                answers=parsed_answers
            )
            self.app.database.questions.append(question)
            return question

    async def list_questions(
            self, theme_id: Optional[int] = None
    ) -> list[Question]:
        if theme_id:
            return [
                question for question in self.app.database.questions
                if question.theme_id == int(theme_id)
            ]
        else:
            return self.app.database.questions
