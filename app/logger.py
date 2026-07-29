import logging
import os


def setup_logger(log_file="calculator.log"):
    """Create and configure the calculator application logger."""

    absolute_log_file = os.path.abspath(log_file)
    log_directory = os.path.dirname(absolute_log_file)

    if log_directory:
        os.makedirs(log_directory, exist_ok=True)

    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Remove file handlers that point to a different log file.
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            handler_path = os.path.abspath(handler.baseFilename)

            if handler_path != absolute_log_file:
                handler.close()
                logger.removeHandler(handler)

    # Add a handler only if this log file is not already configured.
    has_matching_handler = any(
        isinstance(handler, logging.FileHandler)
        and os.path.abspath(handler.baseFilename) == absolute_log_file
        for handler in logger.handlers
    )

    if not has_matching_handler:
        file_handler = logging.FileHandler(
            absolute_log_file,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger