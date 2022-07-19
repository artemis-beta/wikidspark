import re


def is_item(item_id: str) -> bool:
    if not isinstance(item_id, str):
        raise TypeError(
            f"Expected string for item_id by got {type(item_id)} '{item_id}'"
        )
    return len(re.findall(r"Q\d+", item_id)) > 0


def is_property(item_id: str) -> bool:
    return len(re.findall(r"P\d+", item_id)) > 0


def check_id(item_id: str) -> bool:
    """Check ID is the valid form for Wikidata"""
    return is_item(item_id) or is_property(item_id)
