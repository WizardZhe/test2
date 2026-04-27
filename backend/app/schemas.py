from pydantic import BaseModel, Field


class MetricQueryRequest(BaseModel):
    metric_id: str
    filters: dict = Field(default_factory=dict)


class KnowledgeSearchRequest(BaseModel):
    query: str
    top_k: int = 5


class McpCallRequest(BaseModel):
    tool_name: str
    arguments: dict = Field(default_factory=dict)
