from pydantic import BaseModel, ConfigDict, Field
from ._base import ToolResult


class IndividualStudentsOptions(BaseModel):
    model_config = ConfigDict(extra="allow")
    studentIds: list[str] | None = None


class Form(BaseModel):
    model_config = ConfigDict(extra="allow")
    formUrl: str | None = None
    title: str | None = None
    responseUrl: str | None = None
    thumbnailUrl: str | None = None


class GeminiGem(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    url: str | None = None
    title: str | None = None


class Link(BaseModel):
    model_config = ConfigDict(extra="allow")
    url: str | None = None
    thumbnailUrl: str | None = None
    title: str | None = None


class NotebookLmNotebook(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    url: str | None = None
    title: str | None = None


class DriveFile(BaseModel):
    model_config = ConfigDict(extra="allow")
    title: str | None = None
    alternateLink: str | None = None
    thumbnailUrl: str | None = None
    id: str | None = None


class SharedDriveFile(BaseModel):
    model_config = ConfigDict(extra="allow")
    driveFile: DriveFile | None = None
    shareMode: str | None = Field(default=None, description="One of: UNKNOWN_SHARE_MODE, VIEW, EDIT, STUDENT_COPY.")


class YouTubeVideo(BaseModel):
    model_config = ConfigDict(extra="allow")
    alternateLink: str | None = None
    title: str | None = None
    id: str | None = None
    thumbnailUrl: str | None = None


class Material(BaseModel):
    model_config = ConfigDict(extra="allow")
    youtubeVideo: YouTubeVideo | None = None
    driveFile: SharedDriveFile | None = None
    notebook: NotebookLmNotebook | None = None
    link: Link | None = None
    gem: GeminiGem | None = None
    form: Form | None = None


class Announcement(BaseModel):
    model_config = ConfigDict(extra="allow")
    updateTime: str | None = None
    individualStudentsOptions: IndividualStudentsOptions | None = None
    courseId: str | None = None
    state: str | None = Field(default=None, description="One of: PUBLISHED, DRAFT, DELETED.")
    assigneeMode: str | None = Field(default=None, description="One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS.")
    creationTime: str | None = None
    alternateLink: str | None = None
    text: str | None = None
    scheduledTime: str | None = None
    id: str | None = None
    materials: list[Material] | None = None
    creatorUserId: str | None = None


class ListAnnouncementsData(BaseModel):
    model_config = ConfigDict(extra="allow")
    announcements: list[Announcement] | None = None
    nextPageToken: str | None = None


class CreateAnnouncementData(Announcement):
    pass


class CreateAnnouncementResult(ToolResult):
    data: CreateAnnouncementData | None = None


class DeleteAnnouncementData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    courseId: str | None = None
    id: str | None = None


class DeleteAnnouncementResult(ToolResult):
    data: DeleteAnnouncementData | None = None


class GetAnnouncementData(Announcement):
    pass


class GetAnnouncementResult(ToolResult):
    data: GetAnnouncementData | None = None


class ListAnnouncementsResult(ToolResult):
    data: ListAnnouncementsData | None = None


class ModifyAnnouncementAssigneesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: Announcement
    after: Announcement


class ModifyAnnouncementAssigneesResult(ToolResult):
    data: ModifyAnnouncementAssigneesData | None = None


class UpdateAnnouncementData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: Announcement
    after: Announcement


class UpdateAnnouncementResult(ToolResult):
    data: UpdateAnnouncementData | None = None
