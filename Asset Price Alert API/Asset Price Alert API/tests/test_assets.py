def register_and_login(client, email: str, password: str) -> str:
    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Asset User",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return login_response.json()["access_token"]


def test_create_tracked_asset_returns_created_asset(
    client,
    unique_email,
    test_password,
):
    token = register_and_login(
        client=client,
        email=unique_email,
        password=test_password,
    )

    response = client.post(
        "/tracked-assets",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "symbol": "btc",
            "name": "Bitcoin",
            "target_price": "70000",
            "condition": "below",
            "currency": "usd",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["symbol"] == "BTC"
    assert data["name"] == "Bitcoin"
    assert data["target_price"] == "70000.00000000"
    assert data["condition"] == "below"
    assert data["currency"] == "USD"
    assert data["is_active"] is True


def test_list_tracked_assets_returns_user_assets(
    client,
    unique_email,
    test_password,
):
    token = register_and_login(
        client=client,
        email=unique_email,
        password=test_password,
    )

    client.post(
        "/tracked-assets",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "symbol": "ETH",
            "name": "Ethereum",
            "target_price": "4000",
            "condition": "below",
            "currency": "USD",
        },
    )

    response = client.get(
        "/tracked-assets",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["symbol"] == "ETH"


def test_manual_price_check_creates_price_history(
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

    check_response = client.post(
        f"/tracked-assets/{asset_id}/check-now",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert check_response.status_code == 200

    check_data = check_response.json()

    assert check_data["alert_triggered"] is True
    assert check_data["price_check"]["price"] == "68000.00000000"
    assert check_data["price_check"]["source"] == "mock"

    history_response = client.get(
        f"/tracked-assets/{asset_id}/price-history",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert history_response.status_code == 200

    history_data = history_response.json()

    assert len(history_data) == 1
    assert history_data[0]["price"] == "68000.00000000"


def test_create_tracked_asset_requires_authentication(client):
    response = client.post(
        "/tracked-assets",
        json={
            "symbol": "BTC",
            "name": "Bitcoin",
            "target_price": "70000",
            "condition": "below",
            "currency": "USD",
        },
    )

    assert response.status_code in [401, 403]