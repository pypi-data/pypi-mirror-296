import logging
from pathlib import Path
from typing import Optional, Union

__all__ = ["get_logger", "setup_logger"]

LOGGER_NAME = 'psy'

logger = logging.getLogger(LOGGER_NAME)


def get_logger() -> logging.Logger:
    """
    Retrieve the logger instance for the application.
    
    Returns
    -------
    logging.Logger
        The logger instance.
    """
    return logger


def setup_logger(level: int = logging.INFO, 
                 formatter: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                 filename: Optional[Union[str, Path]] = None,
                 console: bool = True,
                 ) -> logging.Logger:
    """
    Set up the logger with the specified configuration.
    
    Parameters
    ----------
    level : int, optional
        The logging level (e.g., logging.INFO, logging.DEBUG), by default logging.INFO.
    formatter : str, optional
        The format string for log messages, by default '%(asctime)s - %(name)s - %(levelname)s - %(message)s'.
    filename : Optional[Union[str, Path]], optional
        If provided, logs will be written to this file, by default None.
    console : bool, optional
        If True, logs will also be displayed in the console, by default True.

    Returns
    -------
    logging.Logger
        The configured logger instance.
    """
    logger.setLevel(level)
    formatter = logging.Formatter(formatter)
    
    # Add console logging if required
    if console:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    # Add file logging if filename is provided
    if filename: 
        fh = logging.FileHandler(filename=filename)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def reset_logger():
    """
    Reset the logger to its default configuration by removing all handlers.
    
    This function ensures that the logger goes back to its initial state, 
    without any added handlers or modified configurations. 
    """
    # Clear all handlers associated with the logger
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    # Reset to default level and configuration
    logger.setLevel(logging.NOTSET)
    logger.addHandler(logging.StreamHandler())
