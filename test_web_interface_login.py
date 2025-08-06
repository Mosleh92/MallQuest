import json
from web_interface import app, mall_db, translator


def test_password_verification():
    client = app.test_client()

    # Invalid password should be rejected
    response = client.post('/login', json={'user_id': 'demo', 'password': 'wrong'})
    assert response.status_code == 401
    assert translator.gettext('invalid_credentials') in response.get_data(as_text=True)

    # Valid password should log in successfully
    response = client.post('/login', json={'user_id': 'demo', 'password': 'demo123'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['user_id'] == 'demo'
