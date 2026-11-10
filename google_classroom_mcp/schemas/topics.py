from pydantic import BaseModel, ConfigDict
from ._base import ToolResult


class Topic(BaseModel):
    model_config = ConfigDict(extra="allow")
    topicId: str | None = None
    courseId: str | None = None
    name: str | None = None
    updateTime: str | None = None


class ListTopicsData(BaseModel):
    model_config = ConfigDict(extra="allow")
    topic: list[Topic] | None = None
    nextPageToken: str | None = None


class CreateTopicData(Topic):
    pass


class CreateTopicResult(ToolResult):
    data: CreateTopicData | None = None


class DeleteTopicData(BaseModel):
    model_config = ConfigDict(extra="allow")

    deleted: bool
    courseId: str | None = None
    id: str | None = None


class DeleteTopicResult(ToolResult):
    data: DeleteTopicData | None = None


class GetTopicData(Topic):
    pass


class GetTopicResult(ToolResult):
    data: GetTopicData | None = None


class ListTopicsResult(ToolResult):
    data: ListTopicsData | None = None


class UpdateTopicData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: Topic
    after: Topic


class UpdateTopicResult(ToolResult):
    data: UpdateTopicData | None = None
