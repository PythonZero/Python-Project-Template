from barb.container_utils import value_or_raise
import pytest


def test_value_or_raise():
    dictionary = {"a": 1, "b": 2}

    with pytest.raises(KeyError, match="c was not found"):
        value_or_raise(dictionary, "c", "{key} was not found")
