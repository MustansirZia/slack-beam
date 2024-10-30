import json
import os
from typing import Dict

from tweepy import Client


def get_prompts() -> Dict[str, str]:
    with open('x_prompts.json') as fd:
        prompts = json.load(fd)
        return prompts


more_prompt = "Can you please show {count} more ideas?"

client = Client(
    consumer_key=os.environ['X_CONSUMER_KEY'],
    consumer_secret=os.environ['X_CONSUMER_SECRET'],
    access_token=os.environ['X_ACCESS_TOKEN'],
    access_token_secret=os.environ['X_ACCESS_TOKEN_SECRET'],
)


def create_post(post) -> None:
    client.create_tweet(text=post)
