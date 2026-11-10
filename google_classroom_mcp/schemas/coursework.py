from pydantic import BaseModel, ConfigDict, Field
from ._base import ToolResult


class DriveFolder(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    title: str | None = None
    alternateLink: str | None = None


class Assignment(BaseModel):
    model_config = ConfigDict(extra="allow")
    studentWorkFolder: DriveFolder | None = None


class Date(BaseModel):
    model_config = ConfigDict(extra="allow")
    month: int | None = None
    day: int | None = None
    year: int | None = None


class GradeCategory(BaseModel):
    model_config = ConfigDict(extra="allow")
    defaultGradeDenominator: int | None = None
    weight: int | None = None
    name: str | None = None
    id: str | None = None


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


class MultipleChoiceQuestion(BaseModel):
    model_config = ConfigDict(extra="allow")
    choices: list[str] | None = None


class TimeOfDay(BaseModel):
    model_config = ConfigDict(extra="allow")
    hours: int | None = None
    minutes: int | None = None
    seconds: int | None = None
    nanos: int | None = None


class CourseWork(BaseModel):
    model_config = ConfigDict(extra="allow")
    updateTime: str | None = None
    dueTime: TimeOfDay | None = None
    gradeCategory: GradeCategory | None = None
    associatedWithDeveloper: bool | None = None
    alternateLink: str | None = None
    gradingPeriodId: str | None = None
    scheduledTime: str | None = None
    title: str | None = None
    assigneeMode: str | None = Field(default=None, description="One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS.")
    creationTime: str | None = None
    creatorUserId: str | None = None
    maxPoints: float | None = None
    dueDate: Date | None = None
    submissionModificationMode: str | None = Field(default=None, description="One of: MODIFIABLE_UNTIL_TURNED_IN, MODIFIABLE.")
    topicId: str | None = None
    assignment: Assignment | None = None
    workType: str | None = Field(default=None, description="One of: ASSIGNMENT, SHORT_ANSWER_QUESTION, MULTIPLE_CHOICE_QUESTION.")
    materials: list[Material] | None = None
    individualStudentsOptions: IndividualStudentsOptions | None = None
    id: str | None = None
    courseId: str | None = None
    description: str | None = None
    state: str | None = Field(default=None, description="One of: PUBLISHED, DRAFT, DELETED.")
    multipleChoiceQuestion: MultipleChoiceQuestion | None = None


class ListCourseWorkData(BaseModel):
    model_config = ConfigDict(extra="allow")
    courseWork: list[CourseWork] | None = None
    nextPageToken: str | None = None


class CreateCourseWorkData(CourseWork):
    pass


class CreateCourseWorkResult(ToolResult):
    data: CreateCourseWorkData | None = None


class DeleteCourseWorkData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    courseId: str | None = None
    id: str | None = None


class DeleteCourseWorkResult(ToolResult):
    data: DeleteCourseWorkData | None = None


class GetCourseWorkData(CourseWork):
    pass


class GetCourseWorkResult(ToolResult):
    data: GetCourseWorkData | None = None


class ListCourseWorkResult(ToolResult):
    data: ListCourseWorkData | None = None


class ModifyCourseWorkAssigneesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: CourseWork
    after: CourseWork


class ModifyCourseWorkAssigneesResult(ToolResult):
    data: ModifyCourseWorkAssigneesData | None = None


class UpdateCourseWorkData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: CourseWork
    after: CourseWork


class UpdateCourseWorkResult(ToolResult):
    data: UpdateCourseWorkData | None = None
