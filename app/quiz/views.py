from aiohttp.web_response import Response
from aiohttp_apispec import (
    docs, response_schema, request_schema, querystring_schema
)
from app.quiz.models import Answer

from app.quiz.schemes import (
    ThemeIdSchema,
    ThemeListSchema,
    ThemeListResponseSchema,
    ThemeResponseSchema,
    ThemeSchema,
    QuestionListResponseSchema,
    QuestionListSchema,
    QuestionResponseSchema,
    QuestionSchema
)
from app.web.mixins import AuthRequiredMixin
from app.web.app import View
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @docs(
        tags=["themes"],
        summary="Add theme",
        description="Add new theme to database"
    )
    @request_schema(ThemeSchema)
    @response_schema(ThemeResponseSchema, 201)
    async def post(self) -> Response:
        new_theme = self.data["title"]
        theme = await self.store.quizzes.create_theme(title=new_theme)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @docs(
        tags=["themes"],
        summary="List Themes",
        description="Get list of all themes from database"
    )
    @response_schema(ThemeListResponseSchema, 200)
    async def get(self) -> Response:
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(AuthRequiredMixin, View):
    @docs(
        tags=["questions"],
        summary="Add question",
        descrioption="Add new question to database"
    )
    @request_schema(QuestionSchema)
    @response_schema(QuestionResponseSchema)
    async def post(self) -> Response:
        new_question = await self.store.quizzes.create_question(
            title=self.data["title"],
            theme_id=self.data["theme_id"],
            answers=[Answer(**answer) for answer in self.data["answers"]],
        )
        return json_response(data=QuestionSchema().dump(new_question))


class QuestionListView(AuthRequiredMixin, View):
    @docs(
        tags=["questions"],
        summary="List Question",
        description="Get list questions from database"
    )
    @querystring_schema(ThemeIdSchema)
    @response_schema(QuestionListResponseSchema)
    async def get(self):
        theme_id = self.request.query.get("theme_id")
        if theme_id:
            theme_id = int(theme_id)
        questions = await self.store.quizzes.list_questions(theme_id)
        return json_response(
            data=QuestionListSchema().dump({"questions": questions})
        )
