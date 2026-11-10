"""rubrics group: create_rubric, delete_rubric, get_rubric, list_rubrics, update_course_work_rubric, update_rubric"""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.rubrics import (
    CreateRubricData,
    CreateRubricResult,
    DeleteRubricData,
    DeleteRubricResult,
    GetRubricData,
    GetRubricResult,
    ListRubricsData,
    ListRubricsResult,
    Rubric,
    UpdateCourseWorkRubricData,
    UpdateCourseWorkRubricResult,
    UpdateRubricData,
    UpdateRubricResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.rubrics")


def register_rubrics_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_rubric",
        description=(
            "Creates a rubric on a course work item and returns it. The user and course owner need rubric "
            "licensing, and the call must use the OAuth client's project that created the course work."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_rubric(
        course_id: str = Field(description="Identifier of the course."),
        course_work_id: str = Field(description="Identifier of the course work."),
        source_spreadsheet_id: str | None = Field(default=None, description="Input only. Immutable. Google Sheets ID of the spreadsheet. This spreadsheet must contain formatted rubric settings. See [Create or reuse a rubric for an assignment](https://support.google.com/edu/classroom/answer/9335069). Use of this field requires the `https://www.googleapis.com/auth/spreadsheets.readonly` or `https://www.googleapis.com/auth/spreadsheets` scope."),
        criteria: list[dict[str, Any]] | None = Field(default=None, description="List of criteria. Each criterion is a dimension on which performance is rated. Keys: id, title, levels, description."),
    ) -> CreateRubricResult:
        tlog = ToolLogger(logger, "create_rubric")
        if not course_id.strip():
            return _err(CreateRubricResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(CreateRubricResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        body = {k: v for k, v in {"sourceSpreadsheetId": source_spreadsheet_id, "criteria": criteria}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().rubrics().create(courseId=course_id, courseWorkId=course_work_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateRubricResult(success=True, statusCode=status, data=CreateRubricData(**data))
            return _upstream_err(CreateRubricResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateRubricResult, tlog, exc)

    @mcp.tool(
        name="delete_rubric",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a rubric. This "
            "action is irreversible — the rubric and any grading criteria set on it cannot be recovered. NEVER "
            "call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly "
            "what will be deleted and that it is permanent, and wait for their explicit written confirmation "
            "before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_rubric(
        course_id: str = Field(description="Identifier of the course."),
        course_work_id: str = Field(description="Identifier of the course work."),
        rubric_id: str = Field(description="Identifier of the rubric."),
    ) -> DeleteRubricResult:
        tlog = ToolLogger(logger, "delete_rubric")
        if not course_id.strip():
            return _err(DeleteRubricResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(DeleteRubricResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        if not rubric_id.strip():
            return _err(DeleteRubricResult, tlog, "VALIDATION_ERROR", "rubric_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().rubrics().delete(courseId=course_id, courseWorkId=course_work_id, id=rubric_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteRubricResult(success=True, statusCode=status, data=DeleteRubricData(deleted=True, courseId=course_id, courseWorkId=course_work_id, id=rubric_id))
            return _upstream_err(DeleteRubricResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteRubricResult, tlog, exc)

    @mcp.tool(
        name="get_rubric",
        description=(
            "Retrieves one rubric of a course work item by ID and returns its criteria, levels and linked "
            "spreadsheet."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_rubric(
        course_id: str = Field(description="Identifier of the course."),
        course_work_id: str = Field(description="Identifier of the course work."),
        rubric_id: str = Field(description="Identifier of the rubric."),
    ) -> GetRubricResult:
        tlog = ToolLogger(logger, "get_rubric")
        if not course_id.strip():
            return _err(GetRubricResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(GetRubricResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        if not rubric_id.strip():
            return _err(GetRubricResult, tlog, "VALIDATION_ERROR", "rubric_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().rubrics().get(courseId=course_id, courseWorkId=course_work_id, id=rubric_id))
            if 200 <= status < 300:
                tlog.success()
                return GetRubricResult(success=True, statusCode=status, data=GetRubricData(**data))
            return _upstream_err(GetRubricResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetRubricResult, tlog, exc)

    @mcp.tool(
        name="list_rubrics",
        description="Lists the rubrics of a course work item. Returns rubrics plus `nextPageToken` for paging.",
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_rubrics(
        course_id: str = Field(description="Identifier of the course."),
        course_work_id: str = Field(description="Identifier of the course work."),
        page_size: int | None = Field(default=None, description="The maximum number of rubrics to return. If unspecified, at most 1 rubric is returned. The maximum value is 1; values above 1 are coerced to 1."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
    ) -> ListRubricsResult:
        tlog = ToolLogger(logger, "list_rubrics")
        if not course_id.strip():
            return _err(ListRubricsResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(ListRubricsResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageSize": page_size, "pageToken": page_token}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().rubrics().list(courseId=course_id, courseWorkId=course_work_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListRubricsResult(success=True, statusCode=status, data=ListRubricsData(**data))
            return _upstream_err(ListRubricsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListRubricsResult, tlog, exc)

    @mcp.tool(
        name="update_course_work_rubric",
        description=(
            "Updates the rubric of a course work item, found by `rubric_id` if given or else the item's only "
            "rubric, and returns it. Rubric edits are limited once grading has started, and the call must use the "
            "OAuth client's project that created the course work. NOTE: this overwrites the current field values "
            "— the original state is not stored by the API after the call. The response includes both the before "
            "and after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_course_work_rubric(
        course_id: str = Field(description="Identifier of the course."),
        course_work_id: str = Field(description="Identifier of the course work."),
        rubric_id: str | None = Field(default=None, description="Optional. Identifier of the rubric."),
        source_spreadsheet_id: str | None = Field(default=None, description="Input only. Immutable. Google Sheets ID of the spreadsheet. This spreadsheet must contain formatted rubric settings. See [Create or reuse a rubric for an assignment](https://support.google.com/edu/classroom/answer/9335069). Use of this field requires the `https://www.googleapis.com/auth/spreadsheets.readonly` or `https://www.googleapis.com/auth/spreadsheets` scope."),
        criteria: list[dict[str, Any]] | None = Field(default=None, description="List of criteria. Each criterion is a dimension on which performance is rated. Keys: id, title, levels, description."),
        update_mask: str | None = Field(default=None, description="Comma-separated field mask of the fields to update. Omit to update exactly the fields you provide."),
    ) -> UpdateCourseWorkRubricResult:
        tlog = ToolLogger(logger, "update_course_work_rubric")
        if not course_id.strip():
            return _err(UpdateCourseWorkRubricResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(UpdateCourseWorkRubricResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        body = {k: v for k, v in {"sourceSpreadsheetId": source_spreadsheet_id, "criteria": criteria}.items() if v is not None}
        if not body:
            return _err(UpdateCourseWorkRubricResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            query = {k: v for k, v in {"id": rubric_id}.items() if v is not None}
            current, status, retry_after = service.execute(
                lambda s: s.courses().courseWork().rubrics().list(courseId=course_id, courseWorkId=course_work_id)
            )
            if not 200 <= status < 300:
                return _upstream_err(UpdateCourseWorkRubricResult, tlog, status, current, retry_after)
            rubrics = current.get("rubrics", [])
            before_data = next((r for r in rubrics if rubric_id and r.get("id") == rubric_id), rubrics[0] if rubrics else {})
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().updateRubric(courseId=course_id, courseWorkId=course_work_id, **query, updateMask=update_mask or ",".join(body), body=body))
            if 200 <= status < 300:
                tlog.success()
                return UpdateCourseWorkRubricResult(success=True, statusCode=status, data=UpdateCourseWorkRubricData(before=Rubric(**before_data), after=Rubric(**data)))
            return _upstream_err(UpdateCourseWorkRubricResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(UpdateCourseWorkRubricResult, tlog, exc)

    @mcp.tool(
        name="update_rubric",
        description=(
            "Updates a rubric by ID and returns it. Rubric edits are limited once grading has started, and the "
            "call must use the OAuth client's project that created the course work. NOTE: this overwrites the "
            "current field values — the original state is not stored by the API after the call. The response "
            "includes both the before and after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_rubric(
        course_id: str = Field(description="Identifier of the course."),
        course_work_id: str = Field(description="Identifier of the course work."),
        rubric_id: str = Field(description="Optional. Identifier of the rubric."),
        source_spreadsheet_id: str | None = Field(default=None, description="Input only. Immutable. Google Sheets ID of the spreadsheet. This spreadsheet must contain formatted rubric settings. See [Create or reuse a rubric for an assignment](https://support.google.com/edu/classroom/answer/9335069). Use of this field requires the `https://www.googleapis.com/auth/spreadsheets.readonly` or `https://www.googleapis.com/auth/spreadsheets` scope."),
        criteria: list[dict[str, Any]] | None = Field(default=None, description="List of criteria. Each criterion is a dimension on which performance is rated. Keys: id, title, levels, description."),
        update_mask: str | None = Field(default=None, description="Comma-separated field mask of the fields to update. Omit to update exactly the fields you provide."),
    ) -> UpdateRubricResult:
        tlog = ToolLogger(logger, "update_rubric")
        if not course_id.strip():
            return _err(UpdateRubricResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(UpdateRubricResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        if not rubric_id.strip():
            return _err(UpdateRubricResult, tlog, "VALIDATION_ERROR", "rubric_id must not be empty", 400)
        body = {k: v for k, v in {"sourceSpreadsheetId": source_spreadsheet_id, "criteria": criteria}.items() if v is not None}
        if not body:
            return _err(UpdateRubricResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().courseWork().rubrics().get(courseId=course_id, courseWorkId=course_work_id, id=rubric_id))
            if not 200 <= status < 300:
                return _upstream_err(UpdateRubricResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().rubrics().patch(courseId=course_id, courseWorkId=course_work_id, id=rubric_id, updateMask=update_mask or ",".join(body), body=body))
            if 200 <= status < 300:
                tlog.success()
                return UpdateRubricResult(success=True, statusCode=status, data=UpdateRubricData(before=Rubric(**before_data), after=Rubric(**data)))
            return _upstream_err(UpdateRubricResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(UpdateRubricResult, tlog, exc)
