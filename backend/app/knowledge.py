DOCUMENTS = [
    {
        "title": "项目延期处置办法",
        "snippet": "延期项目应提交原因说明、影响评估和整改计划，并按流程完成审批。",
        "source": "制度库/项目管理办法.md",
        "keywords": ["项目", "延期", "处理", "处置", "整改"],
    },
    {
        "title": "项目进度填报规范",
        "snippet": "项目负责人应每周更新建设进度、完成量和风险事项。",
        "source": "制度库/进度管理规范.md",
        "keywords": ["项目", "进度", "填报", "完成量"],
    },
]


def search_public_knowledge(query: str, top_k: int) -> dict:
    scored = sorted(
        DOCUMENTS,
        key=lambda item: sum(1 for keyword in item["keywords"] if keyword in query),
        reverse=True,
    )
    items = [
        {"title": item["title"], "snippet": item["snippet"], "source": item["source"]}
        for item in scored[:top_k]
    ]
    return {"query": query, "items": items}
