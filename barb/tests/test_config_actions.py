import os

from barb.config_actions import (
    load_config,
    load_json,
    ConfigValues,
)
from barb.constants import TEST_CONFIG_FILE_PATH, ROOT_DIR

JSON_PATH = os.path.join(ROOT_DIR, "tests", "test_config.json")
JSON_OUTPUT = {
    "PLATFORM_KEY_COLUMNS": {
        "test_platform": {
            "dttm_col": "recorded_dttm",
            "unique_together": ["name", "points"],
        }
    }
}


def test_load_json():
    json_out = load_json(JSON_PATH)
    assert json_out == JSON_OUTPUT


def test_parse_config_file_json():
    ConfigValues.load(JSON_PATH)
    assert ConfigValues.PLATFORM_KEY_COLUMNS == JSON_OUTPUT["PLATFORM_KEY_COLUMNS"]


def test_load_config():
    load_config(TEST_CONFIG_FILE_PATH)
