from backend.app.errors import AppError


METRICS = {
    "project_status_summary": {
        "metric_id": "project_status_summary",
        "metric_name": "项目状态统计",
        "rows": [
            {"status": "在建", "count": 8},
            {"status": "已完成", "count": 5},
            {"status": "延期", "count": 2},
        ],
    },
    "completion_amount": {
        "metric_id": "completion_amount",
        "metric_name": "完成量统计",
        "rows": [{"period": "2026-Q1", "completed": 128}],
    },
    "construction_progress": {
        "metric_id": "construction_progress",
        "metric_name": "建设进度统计",
        "rows": [{"stage": "总体进度", "progress": 0.76}],
    },
}


def query_metric(metric_id: str) -> dict:
    metric = METRICS.get(metric_id)
    if metric is None:
        raise AppError("METRIC_NOT_FOUND", f"指标不存在: {metric_id}", 404)
    return metric
