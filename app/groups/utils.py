def get_group_ids_from_string(group_ids_str: str) -> list[str]:
    return [int(group_id) for group_id in group_ids_str.split(',')]