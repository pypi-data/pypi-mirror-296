from datetime import datetime

from structlog.typing import EventDict


def add_text_time(_1, _2, event_dict: EventDict) -> EventDict:
    event_dict["time"] = (
        datetime.now().astimezone().isoformat(sep=" ", timespec="microseconds")
    )
    return event_dict
