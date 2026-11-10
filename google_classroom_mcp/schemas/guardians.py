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


class Guardian(BaseModel):
    model_config = ConfigDict(extra="allow")
    guardianId: str | None = None
    guardianProfile: UserProfile | None = None
    invitedEmailAddress: str | None = None
    studentId: str | None = None


class ListGuardiansData(BaseModel):
    model_config = ConfigDict(extra="allow")
    nextPageToken: str | None = None
    guardians: list[Guardian] | None = None


class DeleteGuardianData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    studentId: str | None = None
    guardianId: str | None = None


class DeleteGuardianResult(ToolResult):
    data: DeleteGuardianData | None = None


class GetGuardianData(Guardian):
    pass


class GetGuardianResult(ToolResult):
    data: GetGuardianData | None = None


class ListGuardiansResult(ToolResult):
    data: ListGuardiansData | None = None
