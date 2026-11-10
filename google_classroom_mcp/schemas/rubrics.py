from pydantic import BaseModel, ConfigDict
from ._base import ToolResult


class Level(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    points: float | None = None
    description: str | None = None
    title: str | None = None


class Criterion(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    title: str | None = None
    levels: list[Level] | None = None
    description: str | None = None


class Rubric(BaseModel):
    model_config = ConfigDict(extra="allow")
    updateTime: str | None = None
    courseId: str | None = None
    sourceSpreadsheetId: str | None = None
    criteria: list[Criterion] | None = None
    id: str | None = None
    courseWorkId: str | None = None
    creationTime: str | None = None


class ListRubricsData(BaseModel):
    model_config = ConfigDict(extra="allow")
    rubrics: list[Rubric] | None = None
    nextPageToken: str | None = None


class CreateRubricData(Rubric):
    pass


class CreateRubricResult(ToolResult):
    data: CreateRubricData | None = None


class DeleteRubricData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    courseId: str | None = None
    courseWorkId: str | None = None
    id: str | None = None


class DeleteRubricResult(ToolResult):
    data: DeleteRubricData | None = None


class GetRubricData(Rubric):
    pass


class GetRubricResult(ToolResult):
    data: GetRubricData | None = None


class ListRubricsResult(ToolResult):
    data: ListRubricsData | None = None


class UpdateCourseWorkRubricData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: Rubric
    after: Rubric


class UpdateCourseWorkRubricResult(ToolResult):
    data: UpdateCourseWorkRubricData | None = None


class UpdateRubricData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: Rubric
    after: Rubric


class UpdateRubricResult(ToolResult):
    data: UpdateRubricData | None = None
