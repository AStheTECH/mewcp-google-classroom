from pydantic import BaseModel, ConfigDict, Field
from ._base import ToolResult


class DriveFile(BaseModel):
    model_config = ConfigDict(extra="allow")
    title: str | None = None
    alternateLink: str | None = None
    thumbnailUrl: str | None = None
    id: str | None = None


class Form(BaseModel):
    model_config = ConfigDict(extra="allow")
    formUrl: str | None = None
    title: str | None = None
    responseUrl: str | None = None
    thumbnailUrl: str | None = None


class Link(BaseModel):
    model_config = ConfigDict(extra="allow")
    url: str | None = None
    thumbnailUrl: str | None = None
    title: str | None = None


class YouTubeVideo(BaseModel):
    model_config = ConfigDict(extra="allow")
    alternateLink: str | None = None
    title: str | None = None
    id: str | None = None
    thumbnailUrl: str | None = None


class CourseMaterial(BaseModel):
    model_config = ConfigDict(extra="allow")
    link: Link | None = None
    form: Form | None = None
    driveFile: DriveFile | None = None
    youTubeVideo: YouTubeVideo | None = None


class CourseMaterialSet(BaseModel):
    model_config = ConfigDict(extra="allow")
    materials: list[CourseMaterial] | None = None
    title: str | None = None


class DriveFolder(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    title: str | None = None
    alternateLink: str | None = None


class GradeCategory(BaseModel):
    model_config = ConfigDict(extra="allow")
    defaultGradeDenominator: int | None = None
    weight: int | None = None
    name: str | None = None
    id: str | None = None


class GradebookSettings(BaseModel):
    model_config = ConfigDict(extra="allow")
    calculationType: str | None = Field(default=None, description="One of: TOTAL_POINTS, WEIGHTED_CATEGORIES.")
    displaySetting: str | None = Field(default=None, description="One of: SHOW_OVERALL_GRADE, HIDE_OVERALL_GRADE, SHOW_TEACHERS_ONLY.")
    gradeCategories: list[GradeCategory] | None = None


class Course(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str | None = None
    teacherGroupEmail: str | None = None
    calendarId: str | None = None
    updateTime: str | None = None
    courseGroupEmail: str | None = None
    teacherFolder: DriveFolder | None = None
    creationTime: str | None = None
    gradebookSettings: GradebookSettings | None = None
    guardiansEnabled: bool | None = None
    section: str | None = None
    subject: str | None = None
    room: str | None = None
    courseState: str | None = Field(default=None, description="One of: ACTIVE, ARCHIVED, PROVISIONED, DECLINED, SUSPENDED.")
    id: str | None = None
    description: str | None = None
    descriptionHeading: str | None = None
    ownerId: str | None = None
    alternateLink: str | None = None
    enrollmentCode: str | None = None
    courseMaterialSets: list[CourseMaterialSet] | None = None
    levels: str | None = None


class Date(BaseModel):
    model_config = ConfigDict(extra="allow")
    month: int | None = None
    day: int | None = None
    year: int | None = None


class GradingPeriod(BaseModel):
    model_config = ConfigDict(extra="allow")
    title: str | None = None
    startDate: Date | None = None
    id: str | None = None
    endDate: Date | None = None


class GradingPeriodSettings(BaseModel):
    model_config = ConfigDict(extra="allow")
    applyToExistingCoursework: bool | None = None
    gradingPeriods: list[GradingPeriod] | None = None


class ListCoursesData(BaseModel):
    model_config = ConfigDict(extra="allow")
    nextPageToken: str | None = None
    courses: list[Course] | None = None


class CreateCourseData(Course):
    pass


class CreateCourseResult(ToolResult):
    data: CreateCourseData | None = None


class DeleteCourseData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    id: str | None = None


class DeleteCourseResult(ToolResult):
    data: DeleteCourseData | None = None


class GetCourseData(Course):
    pass


class GetCourseResult(ToolResult):
    data: GetCourseData | None = None


class GetGradingPeriodSettingsData(GradingPeriodSettings):
    pass


class GetGradingPeriodSettingsResult(ToolResult):
    data: GetGradingPeriodSettingsData | None = None


class ListCoursesResult(ToolResult):
    data: ListCoursesData | None = None


class ReplaceCourseData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: Course
    after: Course


class ReplaceCourseResult(ToolResult):
    data: ReplaceCourseData | None = None


class UpdateCourseData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: Course
    after: Course


class UpdateCourseResult(ToolResult):
    data: UpdateCourseData | None = None


class UpdateGradingPeriodSettingsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: GradingPeriodSettings
    after: GradingPeriodSettings


class UpdateGradingPeriodSettingsResult(ToolResult):
    data: UpdateGradingPeriodSettingsData | None = None
