import datetime
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
from loguru import logger
from pydantic_settings import BaseSettings

# Get the project root directory
# This is the directory where the main.py file is located
PROJECT_ROOT = Path().resolve()
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# Get the library root directory
# This is the directory where the library files are located
# TODO: check if this is the correct way to get the library root
# LIBRARY_ROOT = files("homesync_ai")


class Settings(BaseSettings, case_sensitive=False, extra="ignore"):
    """
    Project settings.

    Uses pydantic BaseSettings for loading configuration from environment variables.
    """

    # local IP address of the server
    local_ip: str = os.environ.get("LOCAL_IP", "")
    # Library name (used for logging and storage)
    # TODO: fix this setting to be inmutable
    library_name: str = "homesync_AI"

    # Library name (used for logging and storage)
    # TODO: fix this setting to be inmutable
    library_prefix: str = "hs"

    # # Library version
    # version: str = metadata.version(library_name)

    # Logging configuration
    log_level: str = "INFO"

    # Base folder for storing data
    storage_folder: str = str(PROJECT_ROOT.joinpath(library_prefix, "storage"))

    # Base folder for storing logs (default: hs/logs)
    logs_storage_folder: str = str(PROJECT_ROOT.joinpath(library_prefix, "logs"))
    # Gemini API key
    gemini_api_key: str = os.getenv("GEMINI_API_KEY")

    # model id
    model_id: str = "gemini-2.5-flash-preview-05-20"

    database_url: str = os.getenv("DATABASE_URL")


def config_logger(
    log_level="DEBUG",
    log_retention="7 days",
    log_rotation="00:00",
    stderr_log_level="INFO",
    activate_global_exception_handler=True,
):
    """
    Configures the logger with the library name, log level, retention, and rotation.

    :param log_level: Log level for file output (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    :param log_retention: Log file retention (e.g. '7 days', '30 days').
    :param log_rotation: Log file rotation (e.g. '00:00' for midnight).
    :param stderr_log_level: Log level for the console (DEBUG, INFO, WARNING, ERROR, CRITICAL). If None, disables console output.
    :param activate_global_exception_handler: If True, sets up a global exception handler to log uncaught exceptions.
    :return: None

    Example 1: With console output enabled (default 'INFO' level for console):
    ```python
    config_logger(log_level="DEBUG", log_retention="7 days", log_rotation="00:00", stderr_log_level="INFO")
    ```

    Example 2: Without console output (setting `stderr_log_level=None`):
    ```python
    config_logger(log_level="DEBUG", log_retention="7 days", log_rotation="00:00", stderr_log_level=None)
    ```
    """

    # Logs directory (next to main.py)

    logs_dir = Path(settings.logs_storage_folder)
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Log file path (one log per day)
    date_suffix = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join(logs_dir, f"{settings.library_name}_{date_suffix}.log")

    # Remove previous handlers (by default Loguru writes to console)
    logger.remove()

    # Log to file (daily, rotation at midnight)
    logger.add(
        str(log_file_path),
        rotation=log_rotation,  # Rotation according to the parameter
        retention=log_retention,  # Retention according to the parameter
        compression="zip",  # Compress old logs
        level=log_level,  # Log level for the file according to the parameter
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message} | Module: {module} | Function: {function}",
    )

    # If stderr_log_level is not None, add console output
    if stderr_log_level is not None:
        logger.add(
            sys.stderr,
            level=stderr_log_level,  # Log level for console according to the parameter
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
        )

    if activate_global_exception_handler:
        register_global_exception_handler()

    logger.info(
        f"Log configured: {log_file_path} | Log level: {log_level} | Retention: {log_retention} | Rotation: {log_rotation}"
    )
    logger.info(f"homesync version: {settings.version}")


def register_global_exception_handler():
    """
    Set up a global exception handler to log uncaught exceptions.
    This handler will log the exception type, value, and traceback.
    It will also allow the program to exit gracefully on KeyboardInterrupt (Ctrl+C).
    """

    def exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Allow program to exit on Ctrl+C without stacktrace
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.opt(exception=(exc_type, exc_value, exc_traceback)).error(
            "Uncaught exception"
        )

    sys.excepthook = exception_handler


# Load settings
settings = Settings()

# Remove default logger
logger.remove()
