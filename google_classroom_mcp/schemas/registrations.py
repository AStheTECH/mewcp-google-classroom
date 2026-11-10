from pydantic import BaseModel, ConfigDict, Field
from ._base import ToolResult


class CloudPubsubTopic(BaseModel):
    model_config = ConfigDict(extra="allow")
    topicName: str | None = None


class CourseRosterChangesInfo(BaseModel):
    model_config = ConfigDict(extra="allow")
    courseId: str | None = None


class CourseWorkChangesInfo(BaseModel):
    model_config = ConfigDict(extra="allow")
    courseId: str | None = None


class Feed(BaseModel):
    model_config = ConfigDict(extra="allow")
    feedType: str | None = Field(default=None, description="One of: DOMAIN_ROSTER_CHANGES, COURSE_ROSTER_CHANGES, COURSE_WORK_CHANGES.")
    courseWorkChangesInfo: CourseWorkChangesInfo | None = None
    courseRosterChangesInfo: CourseRosterChangesInfo | None = None


class Registration(BaseModel):
    model_config = ConfigDict(extra="allow")
    registrationId: str | None = None
    expiryTime: str | None = None
    cloudPubsubTopic: CloudPubsubTopic | None = None
    feed: Feed | None = None


class CreateRegistrationData(Registration):
    pass


class CreateRegistrationResult(ToolResult):
    data: CreateRegistrationData | None = None


class DeleteRegistrationData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    registrationId: str | None = None


class DeleteRegistrationResult(ToolResult):
    data: DeleteRegistrationData | None = None
