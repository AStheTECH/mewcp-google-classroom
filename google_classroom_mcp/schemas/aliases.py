from pydantic import BaseModel, ConfigDict
from ._base import ToolResult


class CourseAlias(BaseModel):
    model_config = ConfigDict(extra="allow")
    alias: str | None = None


class ListCourseAliasesData(BaseModel):
    model_config = ConfigDict(extra="allow")
    aliases: list[CourseAlias] | None = None
    nextPageToken: str | None = None


class CreateCourseAliasData(CourseAlias):
    pass


class CreateCourseAliasResult(ToolResult):
    data: CreateCourseAliasData | None = None


class DeleteCourseAliasData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    courseId: str | None = None
    alias: str | None = None


class DeleteCourseAliasResult(ToolResult):
    data: DeleteCourseAliasData | None = None


class ListCourseAliasesResult(ToolResult):
    data: ListCourseAliasesData | None = None
