from datetime import datetime

from py_anime_list_sync.utils.mal_models import (
    Anime,
    Picture,
    AlternativeTitles,
    MyListStatus,
    Statistics,
    Broadcast,
    Season,
)


def parse_anime_response(data: dict) -> Anime:
    """
    Parse JSON response from MyAnimeList API into Anime dataclass.

    Args:
        data: Dictionary containing anime data from API

    Returns:
        Anime: Dataclass instance containing parsed data
    """
    # Parse nested objects first using dict unpacking (**)
    main_picture = Picture(**data['main_picture'])
    alternative_titles = AlternativeTitles(**data['alternative_titles'])
    my_list_status = MyListStatus(
        **{**data['my_list_status'],
           'updated_at': datetime.fromisoformat(data['my_list_status']['updated_at'].replace('Z', '+00:00'))
           }
    )
    start_season = Season(**data['start_season'])
    broadcast = Broadcast(**data['broadcast']) if data.get('broadcast') else None
    statistics = Statistics(**data['statistics'])

    created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
    updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))

    return Anime(
        **{
            **data,
            'main_picture': main_picture,
            'alternative_titles': alternative_titles,
            'my_list_status': my_list_status,
            'start_season': start_season,
            'broadcast': broadcast,
            'statistics': statistics,
            'created_at': created_at,
            'updated_at': updated_at
        }
    )
