def test_ping(app):
    res = app.get('/ping')

    assert res.status_code == 200
    assert res.json() == {'status': 200, 'message': 'pong'}
