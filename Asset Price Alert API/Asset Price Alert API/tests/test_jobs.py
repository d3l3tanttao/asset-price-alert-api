from tests.test_assets import register_and_login


def test_enqueue_price_check_returns_queued_job(
    client,
    unique_email,
    test_password,
):
    token = register_and_login(
        client=client,
        email=unique_email,
        password=test_password,
    )

    create_response = client.post(
        "/tracked-assets",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "symbol": "BTC",
            "name": "Bitcoin",
            "target_price": "70000",
            "condition": "below",
            "currency": "USD",
        },
    )

    asset_id = create_response.json()["id"]

    response = client.post(
        f"/tracked-assets/{asset_id}/enqueue-check",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["status"] == "queued"
    assert data["asset_id"] == asset_id


def test_enqueue_price_check_requires_authentication(client):
    response = client.post("/tracked-assets/1/enqueue-check")

    assert response.status_code in [401, 403]