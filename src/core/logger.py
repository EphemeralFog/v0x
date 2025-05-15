import sys
import logging

from loguru import logger

logger.remove()

logger.add(
    sys.stderr,
    level="INFO",
    format="{level.icon} <green>[{time:YYYY/MM/DD} {time:HH:mm:ss}]</green> | <level>{level:^7}</level> | <cyan>{name}:{line}</cyan> | <level>{message}</level>",
    colorize=True
)

logger.add(
    "logs/app.log",
    level="DEBUG",
    format="{level.icon} {time:YYYY-MM-DD HH:mm:ss.SSS} | {level:^7} | {name}:{function}:{line} | {message}",
    rotation="1 MB",  # Rotate after 1 MB
    retention="1 day",  # Keep logs for 1 day
    compression="zip",  # Compress rotated files
    enqueue=True,  # Asynchronous logging
    backtrace=True,
    diagnose=True
)

# Intercept standard logging
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        loguru_opt_depth = 6
        inspect_frame = sys._getframe(loguru_opt_depth) # Start inspecting from this frame upwards

        while inspect_frame and inspect_frame.f_code.co_filename == logging.__file__:
            inspect_frame = inspect_frame.f_back
            loguru_opt_depth += 1

        logger.opt(depth=loguru_opt_depth, exception=record.exc_info).log(level, record.getMessage())


# Example usage (optional, can be removed)
# logger.debug("This is a debug message.")
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
# logger.critical("This is a critical message.")

# You can export the logger instance to be used in other modules
# For example:
# from .logger import logger
# logger.info("Logging from another module!")

