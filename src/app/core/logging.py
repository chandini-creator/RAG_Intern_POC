import logging
import sys

def setup_logging(level: str = "INFO") -> None:
    """
    Standard logging config:
    - logs to stdout
    - includes timestamps + log level + module name
    """
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
