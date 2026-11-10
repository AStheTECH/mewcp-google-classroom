from typing import Any
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


class Attachment(BaseModel):
    model_config = ConfigDict(extra="allow")
    youTubeVideo: YouTubeVideo | None = None
    driveFile: DriveFile | None = None
    link: Link | None = None
    form: Form | None = None


class AssignmentSubmission(BaseModel):
    model_config = ConfigDict(extra="allow")
    attachments: list[Attachment] | None = None


class MultipleChoiceSubmission(BaseModel):
    model_config = ConfigDict(extra="allow")
    answer: str | None = None


class ShortAnswerSubmission(BaseModel):
    model_config = ConfigDict(extra="allow")
    answer: str | None = None


class GradeHistory(BaseModel):
    model_config = ConfigDict(extra="allow")
    maxPoints: float | None = None
    gradeTimestamp: str | None = None
    actorUserId: str | None = None
    pointsEarned: float | None = None
    gradeChangeType: str | None = Field(default=None, description="One of: UNKNOWN_GRADE_CHANGE_TYPE, DRAFT_GRADE_POINTS_EARNED_CHANGE, ASSIGNED_GRADE_POINTS_EARNED_CHANGE, MAX_POINTS_CHANGE.")


class StateHistory(BaseModel):
    model_config = ConfigDict(extra="allow")
    actorUserId: str | None = None
    state: str | None = Field(default=None, description="One of: CREATED, TURNED_IN, RETURNED, RECLAIMED_BY_STUDENT, STUDENT_EDITED_AFTER_TURN_IN.")
    stateTimestamp: str | None = None


class SubmissionHistory(BaseModel):
    model_config = ConfigDict(extra="allow")
    stateHistory: StateHistory | None = None
    gradeHistory: GradeHistory | None = None


class StudentSubmission(BaseModel):
    model_config = ConfigDict(extra="allow")
    courseWorkId: str | None = None
    assignedGrade: float | None = None
    updateTime: str | None = None
    alternateLink: str | None = None
    courseId: str | None = None
    courseWorkType: str | None = Field(default=None, description="One of: ASSIGNMENT, SHORT_ANSWER_QUESTION, MULTIPLE_CHOICE_QUESTION.")
    shortAnswerSubmission: ShortAnswerSubmission | None = None
    userId: str | None = None
    draftRubricGrades: dict[str, Any] | None = None
    creationTime: str | None = None
    assignedRubricGrades: dict[str, Any] | None = None
    state: str | None = Field(default=None, description="One of: NEW, CREATED, TURNED_IN, RETURNED, RECLAIMED_BY_STUDENT.")
    draftGrade: float | None = None
    id: str | None = None
    late: bool | None = None
    submissionHistory: list[SubmissionHistory] | None = None
    associatedWithDeveloper: bool | None = None
    multipleChoiceSubmission: MultipleChoiceSubmission | None = None
    assignmentSubmission: AssignmentSubmission | None = None


class ListStudentSubmissionsData(BaseModel):
    model_config = ConfigDict(extra="allow")
    nextPageToken: str | None = None
    studentSubmissions: list[StudentSubmission] | None = None


class GetStudentSubmissionData(StudentSubmission):
    pass


class GetStudentSubmissionResult(ToolResult):
    data: GetStudentSubmissionData | None = None


class ListStudentSubmissionsResult(ToolResult):
    data: ListStudentSubmissionsData | None = None


class ModifyStudentSubmissionAttachmentsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: StudentSubmission
    after: StudentSubmission


class ModifyStudentSubmissionAttachmentsResult(ToolResult):
    data: ModifyStudentSubmissionAttachmentsData | None = None


class ReclaimStudentSubmissionData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: StudentSubmission
    after: StudentSubmission | None = None


class ReclaimStudentSubmissionResult(ToolResult):
    data: ReclaimStudentSubmissionData | None = None


class ReturnStudentSubmissionData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: StudentSubmission
    after: StudentSubmission | None = None


class ReturnStudentSubmissionResult(ToolResult):
    data: ReturnStudentSubmissionData | None = None


class TurnInStudentSubmissionData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: StudentSubmission
    after: StudentSubmission | None = None


class TurnInStudentSubmissionResult(ToolResult):
    data: TurnInStudentSubmissionData | None = None


class UpdateStudentSubmissionData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: StudentSubmission
    after: StudentSubmission


class UpdateStudentSubmissionResult(ToolResult):
    data: UpdateStudentSubmissionData | None = None
