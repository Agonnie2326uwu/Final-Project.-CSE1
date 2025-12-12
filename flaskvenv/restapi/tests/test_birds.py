import json
from app import app

def test_get_all_birds():
    tester = app.test_client()
    response = tester.get('/birds')
    assert response.status_code == 200
