# 政企系统 AI 能力平台

本仓库按 `docs/superpowers/plans/2026-04-24-政企系统-ai项目开发方案.md` 启动开发，当前交付阶段 1 的最小闭环骨架：

- FastAPI 能力服务：健康检查、鉴权上下文、统一错误响应。
- 固定指标接口：项目状态统计、完成量统计、建设进度统计。
- 公有知识库检索接口：使用内置样例文档模拟 Dify 公有知识库检索。
- MCP 工具入口：工具注册与统一调用入口。
- 审计日志：记录用户、工具名、耗时和结果状态。
- 管理后台入口占位页：用于后续 LobeHub 菜单嵌入。

## 运行测试

```bash
python -m pytest tests/test_stage1_mvp.py -q
```

## 本地启动

```bash
python -m uvicorn backend.app.main:app --reload
```

## 调用约定

除 `/health` 外，接口需要通过请求头传入用户上下文：

```text
X-User-Id: u001
X-User-Name: test-user
X-Roles: operator,viewer
X-Department: digital-office
```

## 当前边界

- 暂未接入真实业务数据库，固定指标使用内存样例数据。
- 暂未接入 Dify、LobeHub、SSO，当前保留可替换接口边界。
- 审计日志使用内存存储，服务重启后会清空。
