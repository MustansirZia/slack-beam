import json
import os

from slack_bolt import App

from app.platform.x import get_prompts as get_prompts_for_x, more_prompt as more_prompt_for_x, create_post
from app.language_models import get_raw_posts
from app.storage import save_raw_posts, PostType, get_post_by_id
from app.utilities import generate_id, generate_slack_response_blocks_for_posts, \
    generate_slack_response_blocks_for_post_types

bolt_app = App(
    token=os.environ['SLACK_BOT_TOKEN'],
    signing_secret=os.environ['SLACK_SIGNING_SECRET']
)

POSTS_COUNT_X = 5

COMMAND_GENERATE_POSTS_FOR_X = "/generate-posts-for-x"
ACTION_GENERATE_POSTS_FOR_X = "generate-posts-for-x"
ACTION_GENERATE_MORE_POSTS_FOR_X = "generate-more-posts-for-x"
ACTION_POST_ON_X = "post-on-x"


@bolt_app.command(COMMAND_GENERATE_POSTS_FOR_X)
def generate_post_types_for_x(ack, respond):
    ack()
    try:
        prompts_for_x = get_prompts_for_x()
        blocks = generate_slack_response_blocks_for_post_types(
            {key for key in prompts_for_x},
            ACTION_GENERATE_POSTS_FOR_X,
        )
        respond(blocks=blocks)
    except Exception as e:
        print(e)
        respond('Something bad happened!')


@bolt_app.action(ACTION_GENERATE_POSTS_FOR_X)
def generate_posts_for_x(ack, respond, payload):
    ack()
    try:
        respond("Thinking about this...")
        prompt = payload.get('selected_option', {}).get('value')

        prompts_for_x = get_prompts_for_x()
        if prompt not in prompts_for_x:
            respond('Unknown post type chosen. Please try again.')
            return

        thread_id = generate_id()
        page = 1
        raw_posts = get_raw_posts(thread_id, prompts_for_x[prompt], POSTS_COUNT_X)
        posts = save_raw_posts(raw_posts, PostType.X)
        blocks = generate_slack_response_blocks_for_posts(
            thread_id,
            POSTS_COUNT_X,
            page,
            posts,
            ACTION_GENERATE_MORE_POSTS_FOR_X,
            ACTION_POST_ON_X
        )
        respond(blocks=blocks)
    except Exception as e:
        print(e)
        respond('Something bad happened!')


@bolt_app.action(ACTION_GENERATE_MORE_POSTS_FOR_X)
def generate_more_posts_for_x(ack, respond, payload):
    ack()
    try:
        respond("Sure! Please let me think ...", replace_original=False)
        values = json.loads(payload['value'])
        thread_id = values['thread_id']
        page = values['page']
        raw_posts = get_raw_posts(thread_id, more_prompt_for_x, POSTS_COUNT_X)
        posts = save_raw_posts(raw_posts, PostType.X)
        blocks = generate_slack_response_blocks_for_posts(
            thread_id,
            POSTS_COUNT_X,
            page,
            posts,
            ACTION_GENERATE_MORE_POSTS_FOR_X,
            ACTION_POST_ON_X
        )
        respond(blocks=blocks, replace_original=False)
    except Exception as e:
        print(e)
        respond('Something bad happened!')


@bolt_app.action(ACTION_POST_ON_X)
def post_on_x(ack, respond, payload):
    ack()
    post_id = payload['value']
    post = get_post_by_id(post_id)
    if post is None:
        respond('The post seems to have vanished from the datastore! Please regenerate the posts.',
                replace_original=False)
        return
    create_post(post.text)
    respond(f"{post.text}.\nPosted on X!", replace_original=False)


from flask import Flask, request

app = Flask(__name__)

from slack_bolt.adapter.flask import SlackRequestHandler

handler = SlackRequestHandler(bolt_app)


@app.route("/slack/events", methods=["POST"])
def slack_events():
    # handler runs App's dispatch method
    return handler.handle(request)
