from fastapi.testclient import TestClient

from backend.app.main import create_app


def auth_headers(user_id="u001"):
    return {
        "X-User-Id": user_id,
        "X-User-Name": "test-user",
        "X-Roles": "operator,viewer",
        "X-Department": "digital-office",
    }


def test_health_check_is_public():
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ai-capability-service"}


def test_metric_query_requires_auth_context_and_writes_audit_log():
    client = TestClient(create_app())


    unauthenticated = client.post(
        "/api/v1/metrics/query",
        json={"metric_id": "project_status_summary", "filters": {}},
    )
    assert unauthenticated.status_code == 401
    assert unauthenticated.json() == {
        "error": {"code": "UNAUTHORIZED", "message": "缺少用户身份上下文"}
    }

    response = client.post(
        "/api/v1/metrics/query",
        headers=auth_headers(),
        json={"metric_id": "project_status_summary", "filters": {}},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["metric_id"] == "project_status_summary"
    assert body["metric_name"] == "项目状态统计"
    assert body["rows"] == [
        {"status": "在建", "count": 8},
        {"status": "已完成", "count": 5},
        {"status": "延期", "count": 2},
    ]

    audit_response = client.get("/api/v1/audit/logs", headers=auth_headers())
    assert audit_response.status_code == 200
    logs = audit_response.json()["items"]
    assert len(logs) == 1
    assert logs[0]["user_id"] == "u001"
    assert logs[0]["tool_name"] == "metric_query"
    assert logs[0]["status"] == "success"


def test_unknown_metric_uses_unified_error_response():
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/metrics/query",
        headers=auth_headers(),
        json={"metric_id": "unknown", "filters": {}},
    )

    assert response.status_code == 404
    assert response.json() == {
        "error": {"code": "METRIC_NOT_FOUND", "message": "指标不存在: unknown"}
    }


def test_public_knowledge_search_returns_citations_and_audit_log():
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/knowledge/public/search",
        headers=auth_headers("u002"),
        json={"query": "项目延期怎么处理", "top_k": 2},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "项目延期怎么处理"
    assert body["items"][0]["title"] == "项目延期处置办法"
    assert "延期项目应提交原因说明" in body["items"][0]["snippet"]
    assert body["items"][0]["source"] == "制度库/项目管理办法.md"

    audit_response = client.get("/api/v1/audit/logs", headers=auth_headers("u002"))
    assert audit_response.status_code == 200
    assert audit_response.json()["items"][0]["tool_name"] == "public_knowledge_search"


def test_mcp_tool_registry_and_call_delegate_to_capability_service():
    client = TestClient(create_app())

    registry = client.get("/mcp/tools", headers=auth_headers())
    assert registry.status_code == 200
    tool_names = [tool["name"] for tool in registry.json()["tools"]]
    assert tool_names == ["metric_query", "public_knowledge_search"]

    response = client.post(
        "/mcp/call",
        headers=auth_headers(),
        json={
            "tool_name": "metric_query",
            "arguments": {"metric_id": "completion_amount", "filters": {}},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["tool_name"] == "metric_query"
    assert body["result"]["metric_name"] == "完成量统计"
    assert body["result"]["rows"] == [{"period": "2026-Q1", "completed": 128}]
