from typing import Any, TypedDict


class ToolError(TypedDict):
    error: str


JsonStringToolResponse = str

ApiObjectResponse = dict[str, Any] | ToolError
