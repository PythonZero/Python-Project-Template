"""Holds State based on errors."""
import logging
from typing import Optional


LOGGER = logging.getLogger(__name__)


class ErrorManager:
    """Stores the errors that occur throughout the code.
    Raise the first error if an error exists"""

    error_list = []

    @classmethod
    def error(cls, error: Exception, logger: Optional[logging.Logger]):
        """Stores and logs the error if a previous error hasn't already been raised"""
        cls.error_list.append(error)
        logger = logging if logger else LOGGER
        logger.exception(error)

    @classmethod
    def raise_first(cls):
        """Raises an error if an error occurred throughout the program's execution"""
        if cls.error_list:
            raise cls.error_list[0]

    @classmethod
    def clear(cls):
        """Resets all errors"""
        cls.error_list = []
