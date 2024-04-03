# Similar account pairs

## Overview
This is a service for identifying similar account name pairs from social media posts using the same hashtag.

The input is a json payload containing the following:
- posts: A list of post records, where each record corresponds to one post. Each post record must have the following keys:
  - is_repost
  - hashtags
  - author_id
- accounts: A list of account records, where each record corresponds to one account. Each account record must have the following keys:
  - id
  - screen_name
- hashtag: The hashtag by which to filter posts
- min_similarity: The minimum similarity to determine whether two screen names are similar


The output is a list containing lists of the format [account_id1, account_id2] indicating which accounts have similar screen names

## To run unit tests
From the `app` directory, run:
```commandline
pytest tests
```

## Deploying locally

Install the dependencies in [requirements.txt](./requirements.txt) 
```commandline
pip install -r requirements.txt
```

Navigate inside the `account_similarity` directory and run:
```commandline
uvicorn main:app --reload
```

Open http://localhost:8000 in your web browser. You should see the following message: "Your account similarity service is live!"

## Deploying with Docker

To deploy the service, navigate inside the `account_similarity` directory and run:

```commandline
docker-compose up -d --build
```

Open http://localhost:8000 in your web browser. You should see the following message: "Your account similarity service is live!"

If you don't, check the logs by running:
```commandline
docker logs account_similarity`
```

For any debugging, it may be easier to run the service without the `-d` flag (detached mode):
```commandline
docker-compose up --build
```

To stop the service and remove the container, run:
```commandline
docker compose down
```


## Sample usage

Sample python code using the `requests` library:

```python
import requests
url_get_similar_acct_pairs = "http://0.0.0.0:8000/similar_account_pairs/"

post_data_example = [{"author_id": "a", "is_repost": False, "hashtags": ["#CatLover", "#catlife"]},
                    {"author_id": "b", "is_repost": True, "hashtags": None},
                    {"author_id": "c", "is_repost": False, "hashtags": ["#CatLover"]}]
account_data_example = [{"id": "a", "screen_name": "catlover"}, 
                        {"id": "c", "screen_name": "catluvr"}]
hashtag = "#CatLover"
min_similarity = .7

payload = {"posts": post_data_example,
         "accounts": account_data_example,
         "hashtag": hashtag,
         "min_similarity": min_similarity}

r = requests.get(url = url_get_similar_acct_pairs, json=payload)
response = r.json()
print(response)
```

You should see `[["catluvr","catlover"]]` printed in the console, since these are similar screen names that both used
the same hashtag. 

