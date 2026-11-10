from pydantic import BaseModel, ConfigDict, Field
from ._base import ToolResult


class Invitation(BaseModel):
    model_config = ConfigDict(extra="allow")
    courseId: str | None = None
    role: str | None = Field(default=None, description="One of: STUDENT, TEACHER, OWNER.")
    id: str | None = None
    userId: str | None = None


class ListInvitationsData(BaseModel):
    model_config = ConfigDict(extra="allow")
    nextPageToken: str | None = None
    invitations: list[Invitation] | None = None


class AcceptInvitationData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: Invitation
    accepted: bool = Field(description="True once the invitation is accepted; the invitation is consumed by the call.")


class AcceptInvitationResult(ToolResult):
    data: AcceptInvitationData | None = None


class CreateInvitationData(Invitation):
    pass


class CreateInvitationResult(ToolResult):
    data: CreateInvitationData | None = None


class DeleteInvitationData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    id: str | None = None


class DeleteInvitationResult(ToolResult):
    data: DeleteInvitationData | None = None


class GetInvitationData(Invitation):
    pass


class GetInvitationResult(ToolResult):
    data: GetInvitationData | None = None


class ListInvitationsResult(ToolResult):
    data: ListInvitationsData | None = None
