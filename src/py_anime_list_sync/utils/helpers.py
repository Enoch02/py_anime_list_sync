from enum import Enum
from typing import Type


def get_enum_names(enum_class: Type[Enum]) -> list[str]:
    """
    Get a list of all member names from any Enum class.

    Args:
        enum_class: Any Enum class

    Returns:
        List of member names as strings

    Example:
        class Color(Enum):
            RED = 1
            BLUE = 2

        names = get_enum_names(Color)  # Returns ['RED', 'BLUE']
    """
    return [member.value for member in enum_class]
