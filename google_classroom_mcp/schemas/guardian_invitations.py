from pydantic import BaseModel, ConfigDict, Field
from ._base import ToolResult


class GuardianInvitation(BaseModel):
    model_config = ConfigDict(extra="allow")
    creationTime: str | None = None
    studentId: str | None = None
    invitationId: str | None = None
    state: str | None = Field(default=None, description="One of: PENDING, COMPLETE.")
    invitedEmailAddress: str | None = None


class ListGuardianInvitationsData(BaseModel):
    model_config = ConfigDict(extra="allow")
    guardianInvitations: list[GuardianInvitation] | None = None
    nextPageToken: str | None = None


class CreateGuardianInvitationData(GuardianInvitation):
    pass


class CreateGuardianInvitationResult(ToolResult):
    data: CreateGuardianInvitationData | None = None


class GetGuardianInvitationData(GuardianInvitation):
    pass


class GetGuardianInvitationResult(ToolResult):
    data: GetGuardianInvitationData | None = None


class ListGuardianInvitationsResult(ToolResult):
    data: ListGuardianInvitationsData | None = None


class UpdateGuardianInvitationData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: GuardianInvitation
    after: GuardianInvitation


class UpdateGuardianInvitationResult(ToolResult):
    data: UpdateGuardianInvitationData | None = None
