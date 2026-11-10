"""announcements group: create_announcement, delete_announcement, get_announcement, list_announcements, modify_announcement_assignees, update_announcement"""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.announcements import (
    Announcement,
    CreateAnnouncementData,
    CreateAnnouncementResult,
    DeleteAnnouncementData,
    DeleteAnnouncementResult,
    GetAnnouncementData,
    GetAnnouncementResult,
    ListAnnouncementsData,
    ListAnnouncementsResult,
    ModifyAnnouncementAssigneesData,
    ModifyAnnouncementAssigneesResult,
    UpdateAnnouncementData,
    UpdateAnnouncementResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.announcements")


def register_announcements_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_announcement",
        description=(
            "Creates an announcement in a course and returns it, optionally with materials, a draft/scheduled "
            "state and specific student assignees. Attachments must be visible to the creator."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_announcement(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        individual_students_options: dict[str, Any] | None = Field(default=None, description="Identifiers of students with access to the announcement. This field is set only if `assigneeMode` is `INDIVIDUAL_STUDENTS`. If the `assigneeMode` is `INDIVIDUAL_STUDENTS`, then only students specified in this field can see the announcement. Keys: studentIds."),
        state: str | None = Field(default=None, description="Status of this announcement. If unspecified, the default state is `DRAFT`. One of: PUBLISHED, DRAFT, DELETED."),
        assignee_mode: str | None = Field(default=None, description="Assignee mode of the announcement. If unspecified, the default value is `ALL_STUDENTS`. One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS."),
        text: str | None = Field(default=None, description="Description of this announcement. The text must be a valid UTF-8 string containing no more than 30,000 characters."),
        scheduled_time: str | None = Field(default=None, description="Optional timestamp when this announcement is scheduled to be published."),
        materials: list[dict[str, Any]] | None = Field(default=None, description="Additional materials. Announcements must have no more than 20 material items. Keys: youtubeVideo, driveFile, link."),
    ) -> CreateAnnouncementResult:
        tlog = ToolLogger(logger, "create_announcement")
        if not course_id.strip():
            return _err(CreateAnnouncementResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        body = {k: v for k, v in {"individualStudentsOptions": individual_students_options, "state": state, "assigneeMode": assignee_mode, "text": text, "scheduledTime": scheduled_time, "materials": materials}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().announcements().create(courseId=course_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateAnnouncementResult(success=True, statusCode=status, data=CreateAnnouncementData(**data))
            return _upstream_err(CreateAnnouncementResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateAnnouncementResult, tlog, exc)

    @mcp.tool(
        name="delete_announcement",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes an "
            "announcement. This action is irreversible — the announcement and its materials link cannot be "
            "recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell "
            "the user exactly what will be deleted and that it is permanent, and wait for their explicit written "
            "confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_announcement(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        announcement_id: str = Field(description="Identifier of the announcement to delete. This identifier is a Classroom-assigned identifier."),
    ) -> DeleteAnnouncementResult:
        tlog = ToolLogger(logger, "delete_announcement")
        if not course_id.strip():
            return _err(DeleteAnnouncementResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not announcement_id.strip():
            return _err(DeleteAnnouncementResult, tlog, "VALIDATION_ERROR", "announcement_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().announcements().delete(courseId=course_id, id=announcement_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteAnnouncementResult(success=True, statusCode=status, data=DeleteAnnouncementData(deleted=True, courseId=course_id, id=announcement_id))
            return _upstream_err(DeleteAnnouncementResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteAnnouncementResult, tlog, exc)

    @mcp.tool(
        name="get_announcement",
        description=(
            "Retrieves one announcement of a course by ID and returns its text, state, materials, assignee mode "
            "and timestamps."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_announcement(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        announcement_id: str = Field(description="Identifier of the announcement."),
    ) -> GetAnnouncementResult:
        tlog = ToolLogger(logger, "get_announcement")
        if not course_id.strip():
            return _err(GetAnnouncementResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not announcement_id.strip():
            return _err(GetAnnouncementResult, tlog, "VALIDATION_ERROR", "announcement_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().announcements().get(courseId=course_id, id=announcement_id))
            if 200 <= status < 300:
                tlog.success()
                return GetAnnouncementResult(success=True, statusCode=status, data=GetAnnouncementData(**data))
            return _upstream_err(GetAnnouncementResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetAnnouncementResult, tlog, exc)

    @mcp.tool(
        name="list_announcements",
        description=(
            "Lists announcements in a course, filtered by `announcement_states`. Students only see PUBLISHED "
            "announcements; teachers and domain admins see all. Returns announcements plus `nextPageToken`."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_announcements(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. Zero or unspecified indicates that the server may assign a maximum. The server may return fewer than the specified number of results."),
        order_by: str | None = Field(default=None, description="Optional sort ordering for results. A comma-separated list of fields with an optional sort direction keyword. Supported field is `updateTime`. Supported direction keywords are `asc` and `desc`. If not specified, `updateTime desc` is the default behavior. Examples: `updateTime asc`, `updateTime`"),
        announcement_states: list[str] | None = Field(default=None, description="Restriction on the `state` of announcements returned. If this argument is left unspecified, the default value is `PUBLISHED`. One of: PUBLISHED, DRAFT, DELETED."),
    ) -> ListAnnouncementsResult:
        tlog = ToolLogger(logger, "list_announcements")
        if not course_id.strip():
            return _err(ListAnnouncementsResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageToken": page_token, "pageSize": page_size, "orderBy": order_by, "announcementStates": announcement_states}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().announcements().list(courseId=course_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListAnnouncementsResult(success=True, statusCode=status, data=ListAnnouncementsData(**data))
            return _upstream_err(ListAnnouncementsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListAnnouncementsResult, tlog, exc)

    @mcp.tool(
        name="modify_announcement_assignees",
        description=(
            "Changes the assignee mode of an announcement (all students or specific students) and adds or removes "
            "individual students, then returns the announcement. Only a teacher of the course can call it. NOTE: "
            "this overwrites the current field values — the original state is not stored by the API after the "
            "call. The response includes both the before and after state so you have a full record of what "
            "changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def modify_announcement_assignees(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        announcement_id: str = Field(description="Identifier of the announcement."),
        assignee_mode: str | None = Field(default=None, description="Mode of the announcement describing whether it is accessible by all students or specified individual students. One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS."),
        modify_individual_students_options: dict[str, Any] | None = Field(default=None, description="Set which students can view or cannot view the announcement. Must be specified only when `assigneeMode` is `INDIVIDUAL_STUDENTS`. Keys: addStudentIds, removeStudentIds."),
    ) -> ModifyAnnouncementAssigneesResult:
        tlog = ToolLogger(logger, "modify_announcement_assignees")
        if not course_id.strip():
            return _err(ModifyAnnouncementAssigneesResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not announcement_id.strip():
            return _err(ModifyAnnouncementAssigneesResult, tlog, "VALIDATION_ERROR", "announcement_id must not be empty", 400)
        body = {k: v for k, v in {"assigneeMode": assignee_mode, "modifyIndividualStudentsOptions": modify_individual_students_options}.items() if v is not None}
        if not body:
            return _err(ModifyAnnouncementAssigneesResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().announcements().get(courseId=course_id, id=announcement_id))
            if not 200 <= status < 300:
                return _upstream_err(ModifyAnnouncementAssigneesResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().announcements().modifyAssignees(courseId=course_id, id=announcement_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return ModifyAnnouncementAssigneesResult(success=True, statusCode=status, data=ModifyAnnouncementAssigneesData(before=Announcement(**before_data), after=Announcement(**data)))
            return _upstream_err(ModifyAnnouncementAssigneesResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ModifyAnnouncementAssigneesResult, tlog, exc)

    @mcp.tool(
        name="update_announcement",
        description=(
            "Updates the provided fields of an announcement (text, state, scheduled time) and returns the updated "
            "announcement. NOTE: this overwrites the current field values — the original state is not stored by "
            "the API after the call. The response includes both the before and after state so you have a full "
            "record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_announcement(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        announcement_id: str = Field(description="Identifier of the announcement."),
        individual_students_options: dict[str, Any] | None = Field(default=None, description="Identifiers of students with access to the announcement. This field is set only if `assigneeMode` is `INDIVIDUAL_STUDENTS`. If the `assigneeMode` is `INDIVIDUAL_STUDENTS`, then only students specified in this field can see the announcement. Keys: studentIds."),
        state: str | None = Field(default=None, description="Status of this announcement. If unspecified, the default state is `DRAFT`. One of: PUBLISHED, DRAFT, DELETED."),
        assignee_mode: str | None = Field(default=None, description="Assignee mode of the announcement. If unspecified, the default value is `ALL_STUDENTS`. One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS."),
        text: str | None = Field(default=None, description="Description of this announcement. The text must be a valid UTF-8 string containing no more than 30,000 characters."),
        scheduled_time: str | None = Field(default=None, description="Optional timestamp when this announcement is scheduled to be published."),
        materials: list[dict[str, Any]] | None = Field(default=None, description="Additional materials. Announcements must have no more than 20 material items. Keys: youtubeVideo, driveFile, link."),
        update_mask: str | None = Field(default=None, description="Comma-separated field mask of the fields to update. Omit to update exactly the fields you provide."),
    ) -> UpdateAnnouncementResult:
        tlog = ToolLogger(logger, "update_announcement")
        if not course_id.strip():
            return _err(UpdateAnnouncementResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not announcement_id.strip():
            return _err(UpdateAnnouncementResult, tlog, "VALIDATION_ERROR", "announcement_id must not be empty", 400)
        body = {k: v for k, v in {"individualStudentsOptions": individual_students_options, "state": state, "assigneeMode": assignee_mode, "text": text, "scheduledTime": scheduled_time, "materials": materials}.items() if v is not None}
        if not body:
            return _err(UpdateAnnouncementResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().announcements().get(courseId=course_id, id=announcement_id))
            if not 200 <= status < 300:
                return _upstream_err(UpdateAnnouncementResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().announcements().patch(courseId=course_id, id=announcement_id, updateMask=update_mask or ",".join(body), body=body))
            if 200 <= status < 300:
                tlog.success()
                return UpdateAnnouncementResult(success=True, statusCode=status, data=UpdateAnnouncementData(before=Announcement(**before_data), after=Announcement(**data)))
            return _upstream_err(UpdateAnnouncementResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(UpdateAnnouncementResult, tlog, exc)
