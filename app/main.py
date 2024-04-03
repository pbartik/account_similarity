from typing import Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from constants import REQUIRED_FIELDS_ACCOUNTS, REQUIRED_FIELDS_POSTS
from utils import get_hashtag_accounts, get_similar_screen_names, validate_payload


class Query(BaseModel):
    posts: List[Dict]
    accounts: List[Dict]
    hashtag: str
    min_similarity: float


app = FastAPI()


@app.get("/")
async def root():
    return "Your account similarity service is live!"


@app.get("/similar_account_pairs/")
async def get_similar_account_pairs(query: Query):
    # validate input for posts
    wrong_format_post = validate_payload(
        data=query.posts, required_fields=REQUIRED_FIELDS_POSTS
    )
    if wrong_format_post:
        raise HTTPException(
            status_code=404,
            detail=f"The payload for posts is formatted incorrectly. "
            f"The required fields for every post: `is_repost`, `hashtags`, and `author_id`. "
            f"Sample incorrect payload element: {wrong_format_post}",
        )
    # validate input for accounts
    wrong_format_account = validate_payload(
        data=query.accounts, required_fields=REQUIRED_FIELDS_ACCOUNTS
    )
    if wrong_format_account:
        raise HTTPException(
            status_code=404,
            detail=f"The payload for accounts is formatted incorrectly. "
            f"The required fields for every account: `id` and `screen_name`. "
            f"Sample incorrect payload element: {wrong_format_account}",
        )

    filter_accounts = get_hashtag_accounts(posts=query.posts, hashtag=query.hashtag)
    hashtag_accounts = [acct for acct in query.accounts if acct.get("id") in filter_accounts]
    similar_accounts = get_similar_screen_names(
        accounts=hashtag_accounts, min_similarity=query.min_similarity
    )
    return similar_accounts
