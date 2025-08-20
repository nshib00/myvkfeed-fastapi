from app.groups.models import Groups
from app.groups.service import GroupService
from app.images.models import GroupImages


async def test_add_groups_list(test_user):
    user, _ = test_user
    raw_groups = [
        {"id": 2001, "name": "Group 1", "is_closed": 0, "type": "page"},
        {"id": 2002, "name": "Group 2", "is_closed": 0, "type": "group"},
    ]
    await GroupService.add_groups_list(raw_groups, user_id=user.id)
    first_group = await GroupService.find_one_or_none(source_id=2001)
    second_group = await GroupService.find_one_or_none(source_id=2002)
    
    assert first_group is not None and second_group is not None 
    assert first_group.title == 'Group 1' and second_group.title == 'Group 2'


async def test_groups_update(groups):
    group = groups[0]
    updated_id = await GroupService.update(Groups.id == group.id, title='Updated title')
    assert updated_id == group.id

    updated_group = await GroupService.get_group_by_source_id(group.source_id)
    assert updated_group.title == 'Updated title'


async def test_add_groups_if_not_exist(groups, test_user):
    user, _ = test_user
    new_groups = [
        Groups(source_id=10001, title='Should not be added', user_id=user.id),
        Groups(source_id=30001, title='New group', user_id=user.id),
    ]
    await GroupService.add_groups_if_not_exist(new_groups)

    group = await GroupService.get_group_by_source_id(30001)
    assert group.title == 'New group'


async def test_get_group_by_source_id(groups):
    group = await GroupService.get_group_by_source_id(groups[1].source_id)
    assert group is not None
    assert group.title == groups[1].title


async def test_get_group_with_posts(groups):
    group = await GroupService.get_group_with_posts(groups[0].id)
    assert group is not None
    assert isinstance(group, Groups)
    assert hasattr(group, 'posts')
        

async def test_get_groups_with_images():
    found_groups = await GroupService.get_groups_with_images()
    assert isinstance(found_groups, list)
    assert all(isinstance(g, Groups) for g in found_groups)
    assert all(
        g.group_image is not None and isinstance(g.group_image, GroupImages)
        for g in found_groups
    )
