from pydantic import BaseModel, ConfigDict
from ._base import ToolResult


class StudentGroup(BaseModel):
    model_config = ConfigDict(extra="allow")
    courseId: str | None = None
    title: str | None = None
    id: str | None = None


class ListStudentGroupsData(BaseModel):
    model_config = ConfigDict(extra="allow")
    studentGroups: list[StudentGroup] | None = None
    nextPageToken: str | None = None


class CreateStudentGroupData(StudentGroup):
    pass


class CreateStudentGroupResult(ToolResult):
    data: CreateStudentGroupData | None = None


class DeleteStudentGroupData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    courseId: str | None = None
    id: str | None = None


class DeleteStudentGroupResult(ToolResult):
    data: DeleteStudentGroupData | None = None


class ListStudentGroupsResult(ToolResult):
    data: ListStudentGroupsData | None = None


class UpdateStudentGroupData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: StudentGroup
    after: StudentGroup


class UpdateStudentGroupResult(ToolResult):
    data: UpdateStudentGroupData | None = None
