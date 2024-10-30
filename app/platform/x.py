import os

from tweepy import Client

prompts = {
    'Joyful': "I need your help in writing a post for X which "
              "should be less than 280 characters. Can you suggest {count} ideas about a post "
              "that sounds joyful and fun?"
              "Please note that each "
              "post should have 2-3 relevant hashtags and 0-1 emojis",
    'Suspenseful': "I need your help in writing a post for X which "
                   "should be less than 280 characters. Can you suggest {count} ideas about a post "
                   "that suits a suspense novel called Goosebumps? "
                   "Please note that each post should have 2-3 relevant hashtags and 0-1 emojis. ",
    'Funny': "I need your help in writing a joke for X which "
             "should be less than 280 characters. Can you suggest {count} jokes that are suitable for all "
             "audiences? "
             "Please note that each joke should have 2-3 relevant hashtags and 0-1 emojis. "
}

more_prompt = "Can you please show {count} more ideas?"

client = Client(
    consumer_key=os.environ['X_CONSUMER_KEY'],
    consumer_secret=os.environ['X_CONSUMER_SECRET'],
    access_token=os.environ['X_ACCESS_TOKEN'],
    access_token_secret=os.environ['X_ACCESS_TOKEN_SECRET'],
)


def create_post(post) -> None:
    client.create_tweet(text=post)
