import asyncio
import contextlib
import time
from threading import Thread

from mypy.nodes import Import

from sslog import logger


logger.debug("hello {}", "debug")
logger.info("hello {}", "info")
logger.warn("hello {}", "warn")
logger.warning("hello {}", "warning")
logger.error("hello {}", "error")
logger.fatal("hello {}", "fatal")
logger.critical("hello {}", "critical")

logger.bind(a=1).info("hello {}", "2")

import loguru

loguru.logger.info("hello")
