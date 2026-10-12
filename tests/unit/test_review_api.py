from fastapi.testclient import TestClient

from apps.api.main import app


def test_review_api_ingest_review_and_mock_adapter(tmp_path, monkeypatch):
    monkeypatch.setenv("FDIA_REVIEW_DB", str(tmp_path / "api-review.sqlite3"))
    client = TestClient(app)
    response = client.post(
        "/api/v1/review/ingest-text",
        json={"filename": "sale.txt", "workflow": "sales",
              "text": "Customer: Asha\nModel: Phone\nAmount: 12000"},
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["queued"] == 1
    record_id = payload["records"][0]["id"]

    preview = client.post(f"/api/v1/review/records/{record_id}/preview")
    assert preview.status_code == 200
    assert preview.json()["mode"] == "dry_run"

    blocked = client.post(f"/api/v1/review/records/{record_id}/mock-submit")
    assert blocked.status_code == 200
    assert blocked.json()["success"] is False

    decision = client.post(
        f"/api/v1/review/records/{record_id}/decision",
        json={"reviewer": "tester", "decision": "approve"},
    )
    assert decision.status_code == 200, decision.text
    assert decision.json()["status"] == "approved"

    simulated = client.post(f"/api/v1/review/records/{record_id}/mock-submit")
    assert simulated.status_code == 200
    assert simulated.json()["mode"] == "mock"
    assert simulated.json()["verified"] is False
