from dataclasses import dataclass, field
from time import perf_counter


@dataclass
class AuditEntry:
    user_id: str
    tool_name: str
    status: str
    duration_ms: int


@dataclass
class AuditStore:
    entries: list[AuditEntry] = field(default_factory=list)

    def record(self, user_id: str, tool_name: str, status: str, started_at: float) -> None:
        self.entries.insert(
            0,
            AuditEntry(
                user_id=user_id,
                tool_name=tool_name,
                status=status,
                duration_ms=max(0, int((perf_counter() - started_at) * 1000)),
            ),
        )

    def list(self) -> list[dict]:
        return [entry.__dict__ for entry in self.entries]
