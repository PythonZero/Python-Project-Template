"""Functions related to logs"""
import os
import sys
import logging

from .config_actions import ConfigValues
from .constants import ROOT_DIR


def create_path_to_file_if_not_exist(filename):
    path_to_file = os.path.abspath(os.path.join(filename, ".."))
    if not os.path.exists(path_to_file):
        os.makedirs(path_to_file)


def start_logging(log_file_path=f"{ROOT_DIR}/logs/logs.log", level=None) -> None:
    """Starts the log"""
    print(f"Logging to {log_file_path}")
    create_path_to_file_if_not_exist(log_file_path)
    level = level if level else getattr(logging, ConfigValues.LOGGING_LEVEL)
    logging.basicConfig(
        filename=log_file_path,
        level=level,
        format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger().addHandler(
        logging.StreamHandler(sys.stdout)
    )  # also output to console.

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger().info("Logging started".center(100, "="))
