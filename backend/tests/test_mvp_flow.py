import os
from datetime import date

os.environ["DATABASE_URL"] = "sqlite:///./test_societydesk.db"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-with-at-least-32-characters"

from fastapi.testclient import TestClient

from app.core.database import Base, engine
from app.main import app


def auth(client: TestClient, email: str, password: str = "password123") -> dict[str, str]:
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_core_mvp_flow() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)

    for payload in [
        {
            "name": "Admin User",
            "email": "admin@societydesk.com",
            "password": "password123",
            "role": "ADMIN",
        },
        {
            "name": "Resident User",
            "email": "resident1@societydesk.com",
            "password": "password123",
            "role": "RESIDENT",
        },
        {
            "name": "Security User",
            "email": "security@societydesk.com",
            "password": "password123",
            "role": "SECURITY",
        },
    ]:
        assert client.post("/auth/register", json=payload).status_code == 201

    admin = auth(client, "admin@societydesk.com")
    resident = auth(client, "resident1@societydesk.com")
    security = auth(client, "security@societydesk.com")

    society = client.post(
        "/admin/societies",
        json={"name": "Green Heights", "address": "MG Road"},
        headers=admin,
    ).json()
    building = client.post(
        "/admin/buildings",
        json={"society_id": society["id"], "name": "A Wing"},
        headers=admin,
    ).json()
    flat = client.post(
        "/admin/flats",
        json={
            "society_id": society["id"],
            "building_id": building["id"],
            "flat_number": "A-101",
            "floor_number": 1,
            "maintenance_amount": "3000.00",
        },
        headers=admin,
    ).json()

    resident_user = client.get("/auth/me", headers=resident).json()
    assert client.post(
        "/admin/residents",
        json={
            "user_id": resident_user["id"],
            "society_id": society["id"],
            "flat_id": flat["id"],
            "phone": "9999999999",
            "is_owner": True,
        },
        headers=admin,
    ).status_code == 201

    assert client.get("/admin/flats", headers=resident).status_code == 403

    generated = client.post(
        "/dues/generate",
        json={
            "society_id": society["id"],
            "month": date.today().month,
            "year": date.today().year,
            "due_date": date.today().isoformat(),
        },
        headers=admin,
    )
    assert generated.status_code == 200, generated.text
    assert generated.json()["created"] == 1
    assert client.post(
        "/dues/generate",
        json={
            "society_id": society["id"],
            "month": date.today().month,
            "year": date.today().year,
            "due_date": date.today().isoformat(),
        },
        headers=admin,
    ).json()["skipped"] == 1

    due = client.get("/dues/my", headers=resident).json()[0]
    payment = client.post(
        f"/dues/{due['id']}/submit-payment",
        data={"amount": "3000.00", "proof_url": "uploads/payments/demo.png"},
        headers=resident,
    )
    assert payment.status_code == 200, payment.text
    assert client.post(f"/dues/{due['id']}/approve", json={"admin_note": "ok"}, headers=admin).status_code == 200

    complaint = client.post(
        "/complaints",
        json={
            "title": "Lift noise",
            "description": "Lift is making a loud sound.",
            "category": "LIFT",
            "priority": "MEDIUM",
        },
        headers=resident,
    )
    assert complaint.status_code == 201, complaint.text
    complaint_id = complaint.json()["id"]
    assert client.patch(
        f"/complaints/{complaint_id}/status",
        json={"status": "IN_PROGRESS", "admin_note": "Assigned"},
        headers=admin,
    ).status_code == 200

    assert client.post(
        "/notices",
        json={"society_id": society["id"], "title": "Water cut", "body": "No water 2-4 PM"},
        headers=admin,
    ).status_code == 201
    assert len(client.get("/notices/active", headers=resident).json()) == 1

    visitor = client.post(
        "/visitors/expected",
        json={
            "visitor_name": "Courier",
            "visitor_phone": "8888888888",
            "purpose": "Delivery",
            "visit_date": date.today().isoformat(),
        },
        headers=resident,
    )
    assert visitor.status_code == 201, visitor.text
    visitor_id = visitor.json()["id"]
    assert len(client.get("/visitors/today", headers=security).json()) == 1
    assert client.post(f"/visitors/{visitor_id}/check-in", headers=security).status_code == 200
    assert client.post(f"/visitors/{visitor_id}/check-out", headers=security).status_code == 200

    assert client.get("/admin/dashboard", headers=admin).status_code == 200
    assert client.get("/resident/dashboard", headers=resident).status_code == 200
    assert client.get("/security/dashboard", headers=security).status_code == 200
