import os

import pytest


@pytest.fixture(scope="session")
def url_api() -> str:
    return os.environ.get("URL_API", "http://localhost:8000")


@pytest.fixture(scope="session")
def url_web() -> str:
    return os.environ.get("URL_WEB", "http://localhost:8080")
