from typing import Sequence, Union
import re

__all__ = [
    "startswith",
]


def startswith(
    string: str,
    patterns: Sequence[str],
    regex: bool = False,
    case: bool = False,
) -> Union[re.Match, bool]:
    if regex:
        flags = re.IGNORECASE if case else 0
        for ptn in patterns:
            obj = re.match(ptn, string, flags)
            if obj:
                return obj
    else:
        string = string.strip()
        for ptn in patterns:
            if string.startswith(str(ptn)):
                return True
    return False
