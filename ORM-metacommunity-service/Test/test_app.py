import pytest
import requests
from app.server.util.logging import logger


def test_my_json_response():
    r = requests.get("http://localhost:8001/api/v1/user/17")
    assert r.status_code == 200
    assert r.json is not None
    logger.info(r.json())
    # assert r.json()[0]['simproId'] is not None
