"""Central logging configuration for MallQuest."""

import logging

LOG_LEVEL = logging.INFO
LOG_FORMAT = "% (asctime)s - %(name)s - %(levelname)s - %(message)s".replace("% ", "%")

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

