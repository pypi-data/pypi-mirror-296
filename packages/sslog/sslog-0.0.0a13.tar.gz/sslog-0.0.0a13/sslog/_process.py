from datetime import datetime

from structlog.typing import EventDict, WrappedLogger


def add_time(_1: WrappedLogger, _2: str, event_dict: EventDict) -> EventDict:
    now = datetime.now()
    event_dict["time"] = now.astimezone().isoformat(timespec="microseconds")
    event_dict["timestamp"] = now.timestamp()
    return event_dict
