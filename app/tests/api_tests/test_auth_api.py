async def test_register_user(client, faker):
    new_name = faker.unique.user_name()
    new_vk_shortname = faker.unique.user_name()
    resp = await client.post(
        "/auth/register",
        json={"name": new_name, "vk_shortname": new_vk_shortname, "password": "testpass"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "registered_user_id" in data


async def test_register_user_already_exists(client, test_user):
    existing_user, _ = test_user
    resp = await client.post(
        "/auth/register",
        json={"name": existing_user.name, "vk_shortname": "dup_vk", "password": "dup"},
    )
    assert resp.status_code == 409


async def test_login_user(client, test_user):
    user, raw_password = test_user
    resp = await client.post(
        "/auth/login",
        json={"name": user.name, "password": raw_password},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert client.cookies.get("myvkfeed_access_token") is not None


async def test_refresh_tokens(client, test_user):
    user, raw_password = test_user
    login_resp = await client.post(
        "/auth/login",
        json={"name": user.name, "password": raw_password},
    )
    assert login_resp.status_code == 200

    refresh_resp = await client.post("/auth/refresh")
    assert refresh_resp.status_code == 200
    data = refresh_resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


async def test_logout_user(client, test_user):
    user, raw_password = test_user
    login_resp = await client.post(
        "/auth/login",
        json={"name": user.name, "password": raw_password},
    )
    assert login_resp.status_code == 200
    assert client.cookies.get("myvkfeed_access_token") is not None

    logout_resp = await client.post("/auth/logout")
    assert logout_resp.status_code == 204
    assert client.cookies.get("myvkfeed_access_token") is None
