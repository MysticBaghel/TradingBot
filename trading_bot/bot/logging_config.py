import logging
import os
from datetime import datetime

LOG_DIR = "logs"


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"trading_bot_{timestamp}.log")

    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),  # also show WARNING+ in console
        ],
    )

    # Suppress console noise — only file gets INFO
    console_handler = logging.root.handlers[1]
    console_handler.setLevel(logging.WARNING)

    logging.info(f"Logging initialized. Log file: {log_file}")
    return log_file
