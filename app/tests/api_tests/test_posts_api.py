# async def test_create_post_with_image(authenticated_client, groups):
#     post_data = {
#         "text": "Test post with image",
#         "vk_id": 12345,
#         "group_id": groups[0].id,
#         "images": ["http://example.com/1.jpg", "http://example.com/2.jpg"]
#     }
#     resp = await authenticated_client.post("/posts", json=post_data)
#     assert resp.status_code in (200, 201)
#     data = resp.json()
#     assert data["text"] == post_data["text"]
#     assert "images" in data
#     assert len(data["images"]) == 2



# async def test_list_posts(authenticated_client, posts):
#     resp = await authenticated_client.get("/posts")
#     assert resp.status_code == 200
#     data = resp.json()
#     assert isinstance(data, list)
#     print(data)
#     print(posts)
#     assert len(data) == len(posts)
#     assert all("id" in p and "text" in p for p in data)