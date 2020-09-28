import json

class TestFlask:
  def test_run_simulation_route(self, app, client):
    res = client.post('/api/v1/run_simulation')
    assert res.status_code == 200
    expected = {"message": "simulation finished running"}
    assert expected == json.loads(res.get_data(as_text=True))