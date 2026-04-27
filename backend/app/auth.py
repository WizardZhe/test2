from fastapi import Header

from backend.app.errors import AppError


def get_auth_context(
    x_user_id: str | None = Header(default=None),
    x_user_name: str | None = Header(default=None),
    x_roles: str | None = Header(default=None),
    x_department: str | None = Header(default=None),
) -> dict:
    if not x_user_id:
        raise AppError("UNAUTHORIZED", "缺少用户身份上下文", 401)

    return {
        "user_id": x_user_id,
        "user_name": x_user_name or x_user_id,
        "roles": [role.strip() for role in (x_roles or "").split(",") if role.strip()],
        "department": x_department or "",
    }
