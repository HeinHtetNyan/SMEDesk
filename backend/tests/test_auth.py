from sqlalchemy import select

from app.models.user import User

SIGNUP_PAYLOAD = {
    "business_name": "Golden Leaf Bakery",
    "owner_email": "owner@goldenleafbakery.mm",
    "owner_password": "test1234",
    "owner_full_name": "Ah Moe",
}


async def test_signup_creates_business_and_owner(client, db_session):
    resp = await client.post("/auth/signup", json=SIGNUP_PAYLOAD)
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]

    user = await db_session.scalar(select(User).where(User.email == SIGNUP_PAYLOAD["owner_email"]))
    assert user is not None
    assert user.role.value == "owner"
    assert user.is_active is True


async def test_signup_rejects_duplicate_email(client):
    first = await client.post("/auth/signup", json=SIGNUP_PAYLOAD)
    assert first.status_code == 200

    second = await client.post("/auth/signup", json=SIGNUP_PAYLOAD)
    assert second.status_code == 400


async def test_signup_rejects_short_password(client):
    payload = {**SIGNUP_PAYLOAD, "owner_password": "short"}
    resp = await client.post("/auth/signup", json=payload)
    assert resp.status_code == 422


async def test_login_succeeds_with_correct_credentials(client):
    await client.post("/auth/signup", json=SIGNUP_PAYLOAD)

    resp = await client.post(
        "/auth/login",
        json={"email": SIGNUP_PAYLOAD["owner_email"], "password": SIGNUP_PAYLOAD["owner_password"]},
    )
    assert resp.status_code == 200
    assert resp.json()["access_token"]


async def test_login_rejects_wrong_password(client):
    await client.post("/auth/signup", json=SIGNUP_PAYLOAD)

    resp = await client.post(
        "/auth/login",
        json={"email": SIGNUP_PAYLOAD["owner_email"], "password": "wrong-password"},
    )
    assert resp.status_code == 401


async def test_login_rejects_unknown_email(client):
    resp = await client.post(
        "/auth/login",
        json={"email": "nobody@goldenleafbakery.mm", "password": "test1234"},
    )
    assert resp.status_code == 401


async def test_login_rejects_deactivated_user(client, db_session):
    await client.post("/auth/signup", json=SIGNUP_PAYLOAD)
    user = await db_session.scalar(select(User).where(User.email == SIGNUP_PAYLOAD["owner_email"]))
    user.is_active = False
    await db_session.commit()

    resp = await client.post(
        "/auth/login",
        json={"email": SIGNUP_PAYLOAD["owner_email"], "password": SIGNUP_PAYLOAD["owner_password"]},
    )
    assert resp.status_code == 401


async def test_me_returns_current_user_with_valid_token(client):
    signup_resp = await client.post("/auth/signup", json=SIGNUP_PAYLOAD)
    token = signup_resp.json()["access_token"]

    resp = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == SIGNUP_PAYLOAD["owner_email"]
    assert body["role"] == "owner"


async def test_me_rejects_missing_token(client):
    resp = await client.get("/auth/me")
    assert resp.status_code == 401


async def test_me_rejects_invalid_token(client):
    resp = await client.get("/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert resp.status_code == 401
