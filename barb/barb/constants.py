"""Contains variables that may be used throughout the app."""
import os

ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, "config", "prod.yaml")
TEST_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, "tests", "test_config.json")
