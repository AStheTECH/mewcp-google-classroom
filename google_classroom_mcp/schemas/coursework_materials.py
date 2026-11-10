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


class CourseWorkMaterial(BaseModel):
    model_config = ConfigDict(extra="allow")
    topicId: str | None = None
    courseId: str | None = None
    materials: list[Material] | None = None
    title: str | None = None
    description: str | None = None
    updateTime: str | None = None
    id: str | None = None
    creatorUserId: str | None = None
    assigneeMode: str | None = Field(default=None, description="One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS.")
    creationTime: str | None = None
    state: str | None = Field(default=None, description="One of: PUBLISHED, DRAFT, DELETED.")
    alternateLink: str | None = None
    individualStudentsOptions: IndividualStudentsOptions | None = None
    scheduledTime: str | None = None


class ListCourseWorkMaterialsData(BaseModel):
    model_config = ConfigDict(extra="allow")
    courseWorkMaterial: list[CourseWorkMaterial] | None = None
    nextPageToken: str | None = None


class CreateCourseWorkMaterialData(CourseWorkMaterial):
    pass


class CreateCourseWorkMaterialResult(ToolResult):
    data: CreateCourseWorkMaterialData | None = None


class DeleteCourseWorkMaterialData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    courseId: str | None = None
    id: str | None = None


class DeleteCourseWorkMaterialResult(ToolResult):
    data: DeleteCourseWorkMaterialData | None = None


class GetCourseWorkMaterialData(CourseWorkMaterial):
    pass


class GetCourseWorkMaterialResult(ToolResult):
    data: GetCourseWorkMaterialData | None = None


class ListCourseWorkMaterialsResult(ToolResult):
    data: ListCourseWorkMaterialsData | None = None


class UpdateCourseWorkMaterialData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: CourseWorkMaterial
    after: CourseWorkMaterial


class UpdateCourseWorkMaterialResult(ToolResult):
    data: UpdateCourseWorkMaterialData | None = None
