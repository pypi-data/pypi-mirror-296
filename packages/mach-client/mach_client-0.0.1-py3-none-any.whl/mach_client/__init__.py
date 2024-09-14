from datetime import datetime
import logging
from pathlib import Path
import sys
from typing import Optional

from . import config


# Exclusive: log to stdout if logging to file?
def make_logger(
    name: str, path: Optional[Path] = None, exclusive=False
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler: logging.Handler = logging.FileHandler(path) if path else logging.StreamHandler(sys.stdout)  # type: ignore
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    if path and not exclusive:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    logger.info(f"START {name} {datetime.today()}\n")

    return logger


path = config.log_files.get("app")

make_logger("mach-client", Path(path) if path else None, True)
