from itertools import combinations
from typing import Dict, List, Tuple

from rapidfuzz.distance.DamerauLevenshtein import normalized_similarity


def validate_payload(data: List[Dict], required_fields: List[str]) -> Dict:
    """
    Validate that every item in a list of dictionaries contains the required keys.
    Otherwise, return the first incorrectly formatted element.

    Parameters
    ----------
    data:
        A list of dictionary records.
        Keys are metadata fields and values are the metadata itself
    required_fields:
        The dictionary keys that every dictionary must contain

    Returns
    -------
    wrong format data:
        The first incorrectly formatted element
    """
    for elem in data:
        if len(set(required_fields).difference(set(elem.keys()))) > 0:
            return elem
    return {}


def get_hashtag_accounts(posts: List[Dict], hashtag: str) -> List[str]:
    """
    From a set of posts, returns the IDs of all accounts that posted a
    particular hashtag (excluding reposts)

    Parameters
    ----------
    posts:
        A list of dictionary records, where each record corresponds to one post.
        Keys are metadata fields for a post, and values are the metadata itself
    hashtag:
        The hashtag by which to filter

    Returns
    -------
    accounts:
        The IDs of all accounts that posted the `hashtag` (excluding reposts)
    """
    result = []
    for post in posts:
        if post["is_repost"]:
            continue

        # assuming we want a case-insensitive search
        # if we want a case-sensitive search, the condition is just `if hashtag in post['hashtags']`
        if (
            hashtag.lower() in [h.lower() for h in post["hashtags"]]
            and post["author_id"] not in result
        ):
            result.append(post["author_id"])

    return result


def get_similar_screen_names(
    accounts: List[Dict], min_similarity: float
) -> List[Tuple[str, str]]:
    """
    From a set of accounts, returns pairs of accounts that have similar screen
    names according to the normalized Damerau-Levenshtein similarity

    Parameters
    ----------
    accounts:
        A list of account records, where each record corresponds to one account.
        Keys are metadata fields for an account, and values are the metadata
        itself
    min_similarity:
        A value between 0 and 1, indicating the minimum similarity needed to
        determine two accounts have similar screen names

    Returns
    -------
    similar_account_pairs:
        A list of tuples of the format (account_id1, account_id2) indicating
        which accounts have similar screen names
    """
    result = []
    screen_names = list(set([acct["screen_name"] for acct in accounts]))
    for pair in combinations(screen_names, 2):
        if normalized_similarity(pair[0], pair[1]) >= min_similarity:
            result.append(pair)
    return result
