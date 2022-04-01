import re

def check_id(item_id: str) -> bool:
    """Check ID is the valid form for Wikidata"""
    return len(re.findall(r'Q\d+', item_id)) > 0
