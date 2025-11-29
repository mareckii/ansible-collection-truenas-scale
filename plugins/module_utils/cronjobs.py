from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional

CRON_FIELDS = ("minute", "hour", "dom", "month", "dow")


def _normalize_cron_value(value: Any) -> str:
    if value is None:
        return "*"
    return str(value)


@dataclass(frozen=True)
class CronSchedule:
    minute: str = "*"
    hour: str = "*"
    dom: str = "*"
    month: str = "*"
    dow: str = "*"

    @classmethod
    def from_mapping(cls, data: Optional[Mapping[str, Any]] = None) -> "CronSchedule":
        if not data:
            return cls()

        kwargs: Dict[str, str] = {}
        for key in CRON_FIELDS:
            if key in data and data[key] is not None:
                kwargs[key] = _normalize_cron_value(data[key])
        return cls(**kwargs)

    def to_api(self) -> Dict[str, str]:
        return {field: getattr(self, field) for field in CRON_FIELDS}

    def matches(self, other: Optional[Mapping[str, Any]]) -> bool:
        other_schedule = {field: "*" for field in CRON_FIELDS}
        if other:
            for field in CRON_FIELDS:
                other_schedule[field] = _normalize_cron_value(other.get(field))
        return other_schedule == self.to_api()


@dataclass(frozen=True)
class CronJobSpec:
    name: str
    command: str
    user: str = "root"
    enabled: bool = True
    schedule: CronSchedule = field(default_factory=CronSchedule)

    @classmethod
    def from_module_params(cls, params: Mapping[str, Any]) -> "CronJobSpec":
        schedule = CronSchedule.from_mapping(params.get("schedule"))
        return cls(
            name=params["name"],
            command=params["command"],
            user=params.get("user") or "root",
            enabled=params.get("enabled", True),
            schedule=schedule,
        )

    def to_payload(self) -> Dict[str, Any]:
        return {
            "description": self.name,
            "command": self.command,
            "user": self.user,
            "enabled": self.enabled,
            "schedule": self.schedule.to_api(),
        }

    def desired_state(self) -> Dict[str, Any]:
        return {
            "description": self.name,
            "command": self.command,
            "user": self.user,
            "enabled": self.enabled,
            "schedule": self.schedule.to_api(),
        }

    def matches(self, job: Optional[Mapping[str, Any]]) -> bool:
        if not job:
            return False

        job_schedule = job.get("schedule")
        return (
            job.get("description") == self.name
            and job.get("command") == self.command
            and job.get("user") == self.user
            and bool(job.get("enabled", True)) == self.enabled
            and self.schedule.matches(job_schedule)
        )

    def diff(self, job: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
        return {
            "before": extract_relevant_job_state(job),
            "after": self.desired_state(),
        }


def extract_relevant_job_state(job: Optional[Mapping[str, Any]]) -> Optional[Dict[str, Any]]:
    if not job:
        return None
    job_schedule = job.get("schedule") or {}
    schedule = {field: _normalize_cron_value(job_schedule.get(field)) for field in CRON_FIELDS}
    return {
        "description": job.get("description"),
        "command": job.get("command"),
        "user": job.get("user"),
        "enabled": bool(job.get("enabled", True)),
        "schedule": schedule,
    }
