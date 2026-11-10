"""Configuration for MewCP Google Classroom MCP Server."""

import logging
import os

SERVER_VERSION = "v2.0.0"
BREAKING_CHANGES: list[dict] = [
    {
        "version": "v2.0.0",
        "summary": (
            "Full rewrite on the typed result envelope. Tools now return {success, statusCode, data, error} "
            "instead of JSON strings; parameter names are snake_case (course_id, page_size, update_mask); "
            "patch_* tools are renamed to update_*; update_course now PATCHes (partial update) and the former "
            "full-replace behaviour moved to replace_course."
        ),
    },
]

# Scopes the tools call (any one per tool is enough; see each tool's upstream docs).
# The Google client libraries manage URLs and the HTTP transport, so no API base or timeouts are set here.
SCOPES = [
    "https://www.googleapis.com/auth/classroom.announcements",
    "https://www.googleapis.com/auth/classroom.announcements.readonly",
    "https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/classroom.coursework.me.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.students",
    "https://www.googleapis.com/auth/classroom.coursework.students.readonly",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
    "https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly",
    "https://www.googleapis.com/auth/classroom.guardianlinks.students",
    "https://www.googleapis.com/auth/classroom.guardianlinks.students.readonly",
    "https://www.googleapis.com/auth/classroom.profile.emails",
    "https://www.googleapis.com/auth/classroom.profile.photos",
    "https://www.googleapis.com/auth/classroom.push-notifications",
    "https://www.googleapis.com/auth/classroom.rosters",
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/classroom.topics",
    "https://www.googleapis.com/auth/classroom.topics.readonly",]


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
