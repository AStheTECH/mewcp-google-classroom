"""coursework_materials group: create_course_work_material, delete_course_work_material, get_course_work_material, list_course_work_materials, update_course_work_material"""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.coursework_materials import (
    CourseWorkMaterial,
    CreateCourseWorkMaterialData,
    CreateCourseWorkMaterialResult,
    DeleteCourseWorkMaterialData,
    DeleteCourseWorkMaterialResult,
    GetCourseWorkMaterialData,
    GetCourseWorkMaterialResult,
    ListCourseWorkMaterialsData,
    ListCourseWorkMaterialsResult,
    UpdateCourseWorkMaterialData,
    UpdateCourseWorkMaterialResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.coursework_materials")


def register_coursework_materials_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_course_work_material",
        description=(
            "Creates a course work material (a classwork item that carries materials but no grade) in a course "
            "and returns it. Attachments must be visible to the creator."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_course_work_material(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        topic_id: str | None = Field(default=None, description="Identifier for the topic that this course work material is associated with. Must match an existing topic in the course."),
        materials: list[dict[str, Any]] | None = Field(default=None, description="Additional materials. A course work material must have no more than 20 material items. Keys: youtubeVideo, driveFile, link."),
        title: str | None = Field(default=None, description="Title of this course work material. The title must be a valid UTF-8 string containing between 1 and 3000 characters."),
        description: str | None = Field(default=None, description="Optional description of this course work material. The text must be a valid UTF-8 string containing no more than 30,000 characters."),
        assignee_mode: str | None = Field(default=None, description="Assignee mode of the course work material. If unspecified, the default value is `ALL_STUDENTS`. One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS."),
        state: str | None = Field(default=None, description="Status of this course work material. If unspecified, the default state is `DRAFT`. One of: PUBLISHED, DRAFT, DELETED."),
        individual_students_options: dict[str, Any] | None = Field(default=None, description="Identifiers of students with access to the course work material. This field is set only if `assigneeMode` is `INDIVIDUAL_STUDENTS`. If the `assigneeMode` is `INDIVIDUAL_STUDENTS`, then only students specified in this field can see the course work material. Keys: studentIds."),
        scheduled_time: str | None = Field(default=None, description="Optional timestamp when this course work material is scheduled to be published."),
    ) -> CreateCourseWorkMaterialResult:
        tlog = ToolLogger(logger, "create_course_work_material")
        if not course_id.strip():
            return _err(CreateCourseWorkMaterialResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        body = {k: v for k, v in {"topicId": topic_id, "materials": materials, "title": title, "description": description, "assigneeMode": assignee_mode, "state": state, "individualStudentsOptions": individual_students_options, "scheduledTime": scheduled_time}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().courseWorkMaterials().create(courseId=course_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateCourseWorkMaterialResult(success=True, statusCode=status, data=CreateCourseWorkMaterialData(**data))
            return _upstream_err(CreateCourseWorkMaterialResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateCourseWorkMaterialResult, tlog, exc)

    @mcp.tool(
        name="delete_course_work_material",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a course work "
            "material. This action is irreversible — the material item and its links to attached materials cannot "
            "be recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell "
            "the user exactly what will be deleted and that it is permanent, and wait for their explicit written "
            "confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_course_work_material(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_material_id: str = Field(description="Identifier of the course work material to delete. This identifier is a Classroom-assigned identifier."),
    ) -> DeleteCourseWorkMaterialResult:
        tlog = ToolLogger(logger, "delete_course_work_material")
        if not course_id.strip():
            return _err(DeleteCourseWorkMaterialResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_material_id.strip():
            return _err(DeleteCourseWorkMaterialResult, tlog, "VALIDATION_ERROR", "course_work_material_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().courseWorkMaterials().delete(courseId=course_id, id=course_work_material_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteCourseWorkMaterialResult(success=True, statusCode=status, data=DeleteCourseWorkMaterialData(deleted=True, courseId=course_id, id=course_work_material_id))
            return _upstream_err(DeleteCourseWorkMaterialResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteCourseWorkMaterialResult, tlog, exc)

    @mcp.tool(
        name="get_course_work_material",
        description=(
            "Retrieves one course work material by ID and returns its title, description, materials, state, topic "
            "and assignee settings."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_course_work_material(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_material_id: str = Field(description="Identifier of the course work material."),
    ) -> GetCourseWorkMaterialResult:
        tlog = ToolLogger(logger, "get_course_work_material")
        if not course_id.strip():
            return _err(GetCourseWorkMaterialResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_material_id.strip():
            return _err(GetCourseWorkMaterialResult, tlog, "VALIDATION_ERROR", "course_work_material_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().courseWorkMaterials().get(courseId=course_id, id=course_work_material_id))
            if 200 <= status < 300:
                tlog.success()
                return GetCourseWorkMaterialResult(success=True, statusCode=status, data=GetCourseWorkMaterialData(**data))
            return _upstream_err(GetCourseWorkMaterialResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetCourseWorkMaterialResult, tlog, exc)

    @mcp.tool(
        name="list_course_work_materials",
        description=(
            "Lists course work materials in a course, filtered by state, linked URL or Drive file ID. Students "
            "only see PUBLISHED materials; teachers and domain admins see all. Returns materials plus "
            "`nextPageToken`."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_course_work_materials(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. Zero or unspecified indicates that the server may assign a maximum. The server may return fewer than the specified number of results."),
        material_link: str | None = Field(default=None, description="Optional filtering for course work material with at least one link material whose URL partially matches the provided string."),
        order_by: str | None = Field(default=None, description="Optional sort ordering for results. A comma-separated list of fields with an optional sort direction keyword. Supported field is `updateTime`. Supported direction keywords are `asc` and `desc`. If not specified, `updateTime desc` is the default behavior. Examples: `updateTime asc`, `updateTime`"),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
        course_work_material_states: list[str] | None = Field(default=None, description="Restriction on the work status to return. Only course work material that matches is returned. If unspecified, items with a work status of `PUBLISHED` is returned. One of: PUBLISHED, DRAFT, DELETED."),
        material_drive_id: str | None = Field(default=None, description="Optional filtering for course work material with at least one Drive material whose ID matches the provided string. If `material_link` is also specified, course work material must have materials matching both filters."),
    ) -> ListCourseWorkMaterialsResult:
        tlog = ToolLogger(logger, "list_course_work_materials")
        if not course_id.strip():
            return _err(ListCourseWorkMaterialsResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageSize": page_size, "materialLink": material_link, "orderBy": order_by, "pageToken": page_token, "courseWorkMaterialStates": course_work_material_states, "materialDriveId": material_drive_id}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().courseWorkMaterials().list(courseId=course_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListCourseWorkMaterialsResult(success=True, statusCode=status, data=ListCourseWorkMaterialsData(**data))
            return _upstream_err(ListCourseWorkMaterialsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListCourseWorkMaterialsResult, tlog, exc)

    @mcp.tool(
        name="update_course_work_material",
        description=(
            "Updates the provided fields of a course work material (title, description, materials, state, "
            "scheduled time, topic) and returns the updated material. NOTE: this overwrites the current field "
            "values — the original state is not stored by the API after the call. The response includes both the "
            "before and after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_course_work_material(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_material_id: str = Field(description="Identifier of the course work material."),
        topic_id: str | None = Field(default=None, description="Identifier for the topic that this course work material is associated with. Must match an existing topic in the course."),
        materials: list[dict[str, Any]] | None = Field(default=None, description="Additional materials. A course work material must have no more than 20 material items. Keys: youtubeVideo, driveFile, link."),
        title: str | None = Field(default=None, description="Title of this course work material. The title must be a valid UTF-8 string containing between 1 and 3000 characters."),
        description: str | None = Field(default=None, description="Optional description of this course work material. The text must be a valid UTF-8 string containing no more than 30,000 characters."),
        assignee_mode: str | None = Field(default=None, description="Assignee mode of the course work material. If unspecified, the default value is `ALL_STUDENTS`. One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS."),
        state: str | None = Field(default=None, description="Status of this course work material. If unspecified, the default state is `DRAFT`. One of: PUBLISHED, DRAFT, DELETED."),
        individual_students_options: dict[str, Any] | None = Field(default=None, description="Identifiers of students with access to the course work material. This field is set only if `assigneeMode` is `INDIVIDUAL_STUDENTS`. If the `assigneeMode` is `INDIVIDUAL_STUDENTS`, then only students specified in this field can see the course work material. Keys: studentIds."),
        scheduled_time: str | None = Field(default=None, description="Optional timestamp when this course work material is scheduled to be published."),
        update_mask: str | None = Field(default=None, description="Comma-separated field mask of the fields to update. Omit to update exactly the fields you provide."),
    ) -> UpdateCourseWorkMaterialResult:
        tlog = ToolLogger(logger, "update_course_work_material")
        if not course_id.strip():
            return _err(UpdateCourseWorkMaterialResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_material_id.strip():
            return _err(UpdateCourseWorkMaterialResult, tlog, "VALIDATION_ERROR", "course_work_material_id must not be empty", 400)
        body = {k: v for k, v in {"topicId": topic_id, "materials": materials, "title": title, "description": description, "assigneeMode": assignee_mode, "state": state, "individualStudentsOptions": individual_students_options, "scheduledTime": scheduled_time}.items() if v is not None}
        if not body:
            return _err(UpdateCourseWorkMaterialResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().courseWorkMaterials().get(courseId=course_id, id=course_work_material_id))
            if not 200 <= status < 300:
                return _upstream_err(UpdateCourseWorkMaterialResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().courseWorkMaterials().patch(courseId=course_id, id=course_work_material_id, updateMask=update_mask or ",".join(body), body=body))
            if 200 <= status < 300:
                tlog.success()
                return UpdateCourseWorkMaterialResult(success=True, statusCode=status, data=UpdateCourseWorkMaterialData(before=CourseWorkMaterial(**before_data), after=CourseWorkMaterial(**data)))
            return _upstream_err(UpdateCourseWorkMaterialResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(UpdateCourseWorkMaterialResult, tlog, exc)
