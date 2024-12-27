import enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


class MALSortOptions(enum.Enum):
    list_score = "list_score"
    last_updated = "list_updated_at"
    title = "anime_title"
    start_date = "anime_start_date"
    id = "anime_id"


class MALStatusFilters(enum.Enum):
    all = "all"
    watching = "watching"
    completed = "completed"
    on_hold = "on_hold"
    dropped_ = "dropped"
    plan_to_watch = "plan_to_watch"


@dataclass
class MALNode:
    id: int
    title: str


@dataclass
class MALAnimeData:
    node: MALNode


@dataclass
class MALPaging:
    next: Optional[str]


@dataclass
class MALAnimeListResponse:
    data: List[MALAnimeData]
    paging: MALPaging


@dataclass
class Picture:
    medium: str
    large: str


@dataclass
class AlternativeTitles:
    synonyms: List[str]
    en: str
    ja: str


@dataclass
class MyListStatus:
    status: str
    score: int
    num_episodes_watched: int
    is_rewatching: bool
    updated_at: datetime
    start_date: str = ""


@dataclass
class Season:
    year: int
    season: str


@dataclass
class Broadcast:
    day_of_the_week: str
    start_time: str


@dataclass
class Statistics:
    status: dict
    num_list_users: int


@dataclass
class Anime:
    id: int
    title: str
    main_picture: Optional[Picture] = None
    alternative_titles: Optional[AlternativeTitles] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    synopsis: Optional[str] = None
    mean: float = 0.0
    rank: int = 0
    popularity: int = 0
    num_list_users: int = 0
    num_scoring_users: int = 0
    nsfw: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    media_type: str = ""
    status: str = ""
    genres: Optional[List[dict]] = None
    my_list_status: Optional[MyListStatus] = None
    num_episodes: int = 0
    start_season: Optional[Season] = None
    broadcast: Optional[Broadcast] = None
    source: str = ""
    average_episode_duration: int = 0
    rating: str = ""
    pictures: Optional[List[dict]] = None
    background: Optional[str] = None
    related_anime: Optional[List[dict]] = None
    related_manga: Optional[List[dict]] = None
    recommendations: Optional[List[dict]] = None
    studios: Optional[List[dict]] = None
    statistics: Optional[Statistics] = None
