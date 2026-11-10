from pydantic import BaseModel, ConfigDict, Field
from ._base import ToolResult


class DriveFolder(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    title: str | None = None
    alternateLink: str | None = None


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


class Student(BaseModel):
    model_config = ConfigDict(extra="allow")
    courseId: str | None = None
    userId: str | None = None
    profile: UserProfile | None = None
    studentWorkFolder: DriveFolder | None = None


class ListStudentsData(BaseModel):
    model_config = ConfigDict(extra="allow")
    nextPageToken: str | None = None
    students: list[Student] | None = None


class CreateStudentData(Student):
    pass


class CreateStudentResult(ToolResult):
    data: CreateStudentData | None = None


class DeleteStudentData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    courseId: str | None = None
    userId: str | None = None


class DeleteStudentResult(ToolResult):
    data: DeleteStudentData | None = None


class GetStudentData(Student):
    pass


class GetStudentResult(ToolResult):
    data: GetStudentData | None = None


class ListStudentsResult(ToolResult):
    data: ListStudentsData | None = None
