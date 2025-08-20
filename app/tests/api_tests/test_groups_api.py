from app.groups.service import GroupService



async def test_get_all_groups(authenticated_client, groups):
    resp = await authenticated_client.get("/groups")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # проверяем, что есть id и title
    assert all("id" in g and "title" in g for g in data)
    # скрытые группы не должны появляться
    assert all(not g.get("is_hidden", False) for g in data)



async def test_get_group_by_id(authenticated_client, groups, group_images):
    group = groups[0]
    resp = await authenticated_client.get(f"/groups/{group.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == group.id
    assert "posts" in data
    assert isinstance(data.get("images", []), list)



async def test_get_group_by_id_not_found(authenticated_client):
    resp = await authenticated_client.get("/groups/999999")
    assert resp.status_code == 404



async def test_hide_and_show_groups(authenticated_client, groups):
    group_ids = [str(groups[0].id), str(groups[1].id)]
    groups_ids_joined = ",".join(group_ids)

    # hide
    resp = await authenticated_client.patch(f"/groups/hide?groups_to_hide={groups_ids_joined}")
    assert resp.status_code == 200
    data = resp.json()
    for group_id in group_ids:
        assert int(group_id) in data["hidden_group_ids"]
        db_group = await GroupService.find_one_or_none(id=int(group_id))
        assert db_group.is_hidden is True

    # show
    resp = await authenticated_client.patch(f"/groups/show?groups_to_show={groups_ids_joined}")
    assert resp.status_code == 200
    data = resp.json()
    for group_id in group_ids:
        assert int(group_id) in data["shown_group_id"]
        db_group = await GroupService.find_one_or_none(id=int(group_id))
        assert db_group.is_hidden is False



async def test_delete_all_groups_as_admin(admin_client, authenticated_client):
    # админ может удалить все группы
    admin_resp = await admin_client.delete("/groups")
    assert admin_resp.status_code == 204

    # обычный пользователь получает 403
    user_resp = await authenticated_client.delete("/groups")
    assert user_resp.status_code == 403




