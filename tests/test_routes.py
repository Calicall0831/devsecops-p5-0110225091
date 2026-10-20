import pytest

from app import create_app


@pytest.fixture
def client():
    return create_app().test_client()


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_crud_flow(client):
    r = client.post("/tasks", json={"title": "Tulis laporan", "priority": "high"})
    assert r.status_code == 201
    tid = r.get_json()["id"]
    assert client.get(f"/tasks/{tid}").status_code == 200
    r = client.put(f"/tasks/{tid}", json={"done": True})
    assert r.get_json()["done"] is True
    assert len(client.get("/tasks?done=true").get_json()) == 1
    assert client.delete(f"/tasks/{tid}").status_code == 204
    assert client.get(f"/tasks/{tid}").status_code == 404


def test_create_invalid(client):
    assert client.post("/tasks", json={}).status_code == 400


def test_update_invalid_and_missing(client):
    assert client.put("/tasks/1", json={"priority": "x"}).status_code == 400
    assert client.put("/tasks/1", json={"done": True}).status_code == 404


def test_delete_missing(client):
    assert client.delete("/tasks/42").status_code == 404


def test_bad_done_param(client):
    assert client.get("/tasks?done=maybe").status_code == 400


def test_stats(client):
    client.post("/tasks", json={"title": "A"})
    assert client.get("/stats").get_json()["total"] == 1
