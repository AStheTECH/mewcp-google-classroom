from pydantic import BaseModel, ConfigDict
from ._base import ToolResult


class StudentGroupMember(BaseModel):
    model_config = ConfigDict(extra="allow")
    studentGroupId: str | None = None
    userId: str | None = None
    courseId: str | None = None


class ListStudentGroupMembersData(BaseModel):
    model_config = ConfigDict(extra="allow")
    nextPageToken: str | None = None
    studentGroupMembers: list[StudentGroupMember] | None = None


class CreateStudentGroupMemberData(StudentGroupMember):
    pass


class CreateStudentGroupMemberResult(ToolResult):
    data: CreateStudentGroupMemberData | None = None


class DeleteStudentGroupMemberData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    courseId: str | None = None
    studentGroupId: str | None = None
    userId: str | None = None


class DeleteStudentGroupMemberResult(ToolResult):
    data: DeleteStudentGroupMemberData | None = None


class ListStudentGroupMembersResult(ToolResult):
    data: ListStudentGroupMembersData | None = None
