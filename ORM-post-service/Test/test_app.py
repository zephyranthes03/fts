import pytest
import requests


def test_my_json_response():
    r = requests.get("http://localhost:8001/api/v1/user/17")
    assert r.status_code == 200
    assert r.json is not None
    print(r.json())
    # assert r.json()[0]['simproId'] is not None
