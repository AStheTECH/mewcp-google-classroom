"""aliases group: create_course_alias, delete_course_alias, list_course_aliases"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.aliases import (
    CreateCourseAliasData,
    CreateCourseAliasResult,
    DeleteCourseAliasData,
    DeleteCourseAliasResult,
    ListCourseAliasesData,
    ListCourseAliasesResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.aliases")


def register_aliases_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_course_alias",
        description=(
            "Creates an alias for a course and returns it. The alias must start with `d:` (domain-scoped) or `p:` "
            "(project-scoped), and fails with ALREADY_EXISTS if it is taken."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_course_alias(
        course_id: str = Field(description="Identifier of the course to alias. This identifier can be either the Classroom-assigned identifier or an alias."),
        alias: str = Field(description="Alias string. The format of the string indicates the desired alias scoping. * `d:` indicates a domain-scoped alias. Example: `d:math_101` * `p:` indicates a project-scoped alias. Example: `p:abc123` This field has a maximum length of 256 characters."),
    ) -> CreateCourseAliasResult:
        tlog = ToolLogger(logger, "create_course_alias")
        if not course_id.strip():
            return _err(CreateCourseAliasResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        body = {k: v for k, v in {"alias": alias}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().aliases().create(courseId=course_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateCourseAliasResult(success=True, statusCode=status, data=CreateCourseAliasData(**data))
            return _upstream_err(CreateCourseAliasResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateCourseAliasResult, tlog, exc)

    @mcp.tool(
        name="delete_course_alias",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a course "
            "alias. This action is irreversible — the alias (the course itself is not deleted) cannot be "
            "recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell "
            "the user exactly what will be deleted and that it is permanent, and wait for their explicit written "
            "confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_course_alias(
        course_id: str = Field(description="Identifier of the course whose alias should be deleted. This identifier can be either the Classroom-assigned identifier or an alias."),
        alias: str = Field(description="Alias to delete. This may not be the Classroom-assigned identifier."),
    ) -> DeleteCourseAliasResult:
        tlog = ToolLogger(logger, "delete_course_alias")
        if not course_id.strip():
            return _err(DeleteCourseAliasResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not alias.strip():
            return _err(DeleteCourseAliasResult, tlog, "VALIDATION_ERROR", "alias must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().aliases().delete(courseId=course_id, alias=alias))
            if 200 <= status < 300:
                tlog.success()
                return DeleteCourseAliasResult(success=True, statusCode=status, data=DeleteCourseAliasData(deleted=True, courseId=course_id, alias=alias))
            return _upstream_err(DeleteCourseAliasResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteCourseAliasResult, tlog, exc)

    @mcp.tool(
        name="list_course_aliases",
        description="Lists the aliases of a course. Returns each alias string plus `nextPageToken` for paging.",
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_course_aliases(
        course_id: str = Field(description="The identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. Zero or unspecified indicates that the server may assign a maximum. The server may return fewer than the specified number of results."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
    ) -> ListCourseAliasesResult:
        tlog = ToolLogger(logger, "list_course_aliases")
        if not course_id.strip():
            return _err(ListCourseAliasesResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageSize": page_size, "pageToken": page_token}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().aliases().list(courseId=course_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListCourseAliasesResult(success=True, statusCode=status, data=ListCourseAliasesData(**data))
            return _upstream_err(ListCourseAliasesResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListCourseAliasesResult, tlog, exc)
