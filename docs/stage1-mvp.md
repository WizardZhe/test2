# 阶段 1 最小闭环交付说明

## 成功标准

用户可通过 MCP 入口调用固定指标查询和公有知识库检索，能力服务记录调用审计日志，并提供管理后台占位入口。

## 已实现

- `GET /health`：服务健康检查。
- `POST /api/v1/metrics/query`：固定高频指标查询。
- `POST /api/v1/knowledge/public/search`：公有知识库检索。
- `GET /api/v1/audit/logs`：审计日志查询。
- `GET /mcp/tools`：MCP 工具注册列表。
- `POST /mcp/call`：MCP 工具统一调用。
- `GET /admin`：管理后台占位入口。

## 验证方式

```bash
python -m pytest tests/test_stage1_mvp.py -q
```

当前测试覆盖：

- 健康检查无需鉴权。
- 指标查询必须带用户上下文。
- 未知指标返回统一错误结构。
- 知识库检索返回来源引用。
- MCP 工具入口可代理能力服务调用。
- 工具调用会写入审计日志。

## 后续替换点

- 将 `backend/app/metrics.py` 的内存指标替换为只读业务数据库查询。
- 将 `backend/app/knowledge.py` 的样例检索替换为 Dify 公有知识库 API。
- 将 `backend/app/audit.py` 的内存日志替换为关系型数据库表。
- 将请求头鉴权替换为 LobeHub/SSO 透传后的统一身份校验。
