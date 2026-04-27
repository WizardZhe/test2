from time import perf_counter

from fastapi import Depends, FastAPI

from backend.app.audit import AuditStore
from backend.app.auth import get_auth_context
from backend.app.errors import AppError, install_error_handlers
from backend.app.knowledge import search_public_knowledge
from backend.app.metrics import query_metric
from backend.app.schemas import KnowledgeSearchRequest, McpCallRequest, MetricQueryRequest


def create_app() -> FastAPI:
    app = FastAPI(title="政企系统 AI 能力服务")
    app.state.audit_store = AuditStore()
    install_error_handlers(app)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "service": "ai-capability-service"}

    @app.post("/api/v1/metrics/query")
    def metrics_query(
        request: MetricQueryRequest,
        auth: dict = Depends(get_auth_context),
    ) -> dict:
        return _run_with_audit(app, auth["user_id"], "metric_query", lambda: query_metric(request.metric_id))

    @app.post("/api/v1/knowledge/public/search")
    def public_knowledge_search(
        request: KnowledgeSearchRequest,
        auth: dict = Depends(get_auth_context),
    ) -> dict:
        return _run_with_audit(
            app,
            auth["user_id"],
            "public_knowledge_search",
            lambda: search_public_knowledge(request.query, request.top_k),
        )

    @app.get("/api/v1/audit/logs")
    def audit_logs(auth: dict = Depends(get_auth_context)) -> dict:
        return {"items": app.state.audit_store.list()}

    @app.get("/mcp/tools")
    def mcp_tools(auth: dict = Depends(get_auth_context)) -> dict:
        return {
            "tools": [
                {"name": "metric_query", "description": "查询固定高频指标"},
                {"name": "public_knowledge_search", "description": "检索公有知识库"},
            ]
        }

    @app.post("/mcp/call")
    def mcp_call(request: McpCallRequest, auth: dict = Depends(get_auth_context)) -> dict:
        if request.tool_name == "metric_query":
            payload = MetricQueryRequest(**request.arguments)
            result = _run_with_audit(
                app,
                auth["user_id"],
                "metric_query",
                lambda: query_metric(payload.metric_id),
            )
        elif request.tool_name == "public_knowledge_search":
            payload = KnowledgeSearchRequest(**request.arguments)
            result = _run_with_audit(
                app,
                auth["user_id"],
                "public_knowledge_search",
                lambda: search_public_knowledge(payload.query, payload.top_k),
            )
        else:
            raise AppError("TOOL_NOT_FOUND", f"工具不存在: {request.tool_name}", 404)

        return {"tool_name": request.tool_name, "result": result}

    @app.get("/admin")
    def admin_placeholder(auth: dict = Depends(get_auth_context)) -> dict:
        return {"name": "政企系统 AI 管理后台", "status": "placeholder"}

    return app


def _run_with_audit(app: FastAPI, user_id: str, tool_name: str, action):
    started_at = perf_counter()
    try:
        result = action()
    except Exception:
        app.state.audit_store.record(user_id, tool_name, "failed", started_at)
        raise

    app.state.audit_store.record(user_id, tool_name, "success", started_at)
    return result


app = create_app()
