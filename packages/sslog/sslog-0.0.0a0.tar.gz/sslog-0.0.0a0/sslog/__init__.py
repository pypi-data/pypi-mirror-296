import json
import logging
import sys
from datetime import datetime

import structlog
from structlog.typing import EventDict, WrappedLogger


if sys.platform != "win32":

    def add_time(_1: WrappedLogger, _2: str, event_dict: EventDict) -> EventDict:
        event_dict["time"] = datetime.now(tz=LocalTimeZone).isoformat(timespec="microseconds")
        return event_dict

    structlog.configure(
        processors=[
            add_time,
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.CallsiteParameterAdder([
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.THREAD,
            ]),
            structlog.dev.set_exc_info,
            structlog.processors.ExceptionRenderer(),
            structlog.processors.EventRenamer("msg"),
            structlog.processors.JSONRenderer(json.dumps, default=str),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )

logger: structlog.stdlib.BoundLogger = structlog.get_logger()
