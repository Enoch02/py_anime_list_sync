import enum
from dataclasses import dataclass


@dataclass
class AuthenticatedAccount:
    id: int
    tracker: str
    account_name: str
    token: str


class SortOptions(enum.Enum):
    list_score = "list_score"
    last_updated = "list_updated_at"
    title = "anime_title"
    start_date = "anime_start_date"
    id = "anime_id"


class StatusFilters(enum.Enum):
    all = "all"
    watching = "watching"
    completed = "completed"
    on_hold = "on_hold"
    dropped_ = "dropped"
    plan_to_watch = "plan_to_watch"
