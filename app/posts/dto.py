from app.posts.models import Posts


class PostsDTO:
    pass
    # def to_model(post_dict: dict) -> Posts:
    #     return Posts(
    #         pub_date=post_dict['date'],
    #         group_id=GroupService.get_group_by_source_id(
    #             source_id=post_dict['source_id']
    #             ),
    #         text=post_dict['text'],
    #     )