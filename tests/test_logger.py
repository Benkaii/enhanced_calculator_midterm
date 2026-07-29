import logging

from app.logger import setup_logger


def get_file_handlers(logger):
    """Return only the logger's file handlers."""

    return [
        handler
        for handler in logger.handlers
        if isinstance(handler, logging.FileHandler)
    ]


def test_setup_logger_creates_logger_and_file(tmp_path):
    log_file = tmp_path / "calculator.log"

    logger = setup_logger(str(log_file))
    file_handlers = get_file_handlers(logger)

    assert logger.name == "calculator"
    assert logger.level == logging.INFO
    assert logger.propagate is False
    assert len(file_handlers) == 1

    logger.info("Test calculation log")

    for handler in file_handlers:
        handler.flush()

    assert log_file.exists()

    log_contents = log_file.read_text(encoding="utf-8")

    assert "INFO" in log_contents
    assert "Test calculation log" in log_contents


def test_setup_logger_reuses_existing_handler(tmp_path):
    log_file = tmp_path / "calculator.log"

    logger = setup_logger(str(log_file))
    original_file_handlers = get_file_handlers(logger)

    same_logger = setup_logger(str(log_file))
    current_file_handlers = get_file_handlers(same_logger)

    assert same_logger is logger
    assert len(current_file_handlers) == 1
    assert current_file_handlers[0] is original_file_handlers[0]