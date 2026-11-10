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


class GetUserProfileData(UserProfile):
    pass


class GetUserProfileResult(ToolResult):
    data: GetUserProfileData | None = None
