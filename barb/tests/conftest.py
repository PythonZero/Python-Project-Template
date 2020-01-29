"""Fixtures that are used in multiple test files."""

import pytest


@pytest.fixture(scope="session")
def something():
    # something tht only runs if passed as a parameter into the function.
    return "something"


@pytest.fixture(scope="session", autouse=True)
def something_that_always_runs():
    # something that always runs
    return "something that always runs"