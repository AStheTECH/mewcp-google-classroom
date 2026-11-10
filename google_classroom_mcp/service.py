"""Upstream API client for MewCP Google Classroom MCP Server."""

import json
import logging
from collections.abc import Callable
from typing import Any

from fastmcp_credentials import get_credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

logger = logging.getLogger("google-classroom-mcp.service")


def get_service() -> Resource:
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")
    return build("classroom", "v1", credentials=Credentials(token=cred.access_token), cache_discovery=False)


def _parse_retry_after(header: str | None) -> int | None:
    if not header:
        return None
    try:
        return int(header)
    except ValueError:
        return None


def _error_message(exc: HttpError) -> str:
    try:
        message = json.loads(exc.content).get("error", {}).get("message")
    except (ValueError, AttributeError, TypeError):
        message = None
    return str(message or exc.reason or f"HTTP {exc.resp.status}")


def execute(call: Callable[[Resource], Any]) -> tuple[dict[str, Any], int, int | None]:
    """Run one Classroom API call; `call` receives the service and returns the request to execute."""
    service = get_service()
    try:
        data = call(service).execute()
        return (data if isinstance(data, dict) else {}), 200, None
    except HttpError as exc:
        status = int(exc.resp.status)
        return {"error": _error_message(exc)}, status, _parse_retry_after(exc.resp.get("retry-after"))
