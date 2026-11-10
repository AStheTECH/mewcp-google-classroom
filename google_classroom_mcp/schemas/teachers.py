from pydantic import BaseModel, ConfigDict, Field
from ._base import ToolResult


class GlobalPermission(BaseModel):
    model_config = ConfigDict(extra="allow")
    permission: str | None = Field(default=None, description="One of: CREATE_COURSE.")


class Name(BaseModel):
    model_config = ConfigDict(extra="allow")
    familyName: str | None = None
    givenName: str | None = None
    fullName: str | None = None


class UserProfile(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    photoUrl: str | None = None
    verifiedTeacher: bool | None = None
    name: Name | None = None
    permissions: list[GlobalPermission] | None = None
    emailAddress: str | None = None


class Teacher(BaseModel):
    model_config = ConfigDict(extra="allow")
    userId: str | None = None
    courseId: str | None = None
    profile: UserProfile | None = None


class ListTeachersData(BaseModel):
    model_config = ConfigDict(extra="allow")
    teachers: list[Teacher] | None = None
    nextPageToken: str | None = None


class CreateTeacherData(Teacher):
    pass


class CreateTeacherResult(ToolResult):
    data: CreateTeacherData | None = None


class DeleteTeacherData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    courseId: str | None = None
    userId: str | None = None


class DeleteTeacherResult(ToolResult):
    data: DeleteTeacherData | None = None


class GetTeacherData(Teacher):
    pass


class GetTeacherResult(ToolResult):
    data: GetTeacherData | None = None


class ListTeachersResult(ToolResult):
    data: ListTeachersData | None = None
