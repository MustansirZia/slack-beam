import json
import uuid
from typing import List, Any, Iterable

from app.storage import Post


def generate_id() -> str:
    return uuid.uuid4().__str__()


def generate_slack_response_blocks_for_post_types(
        types: Iterable[str],
        action: str
) -> List[Any]:
    options = []
    for index, post in sorted(enumerate(types)):
        options.append(
            {
                "text": {
                    "type": "plain_text",
                    "text": f"{index + 1}. {post}",
                },
                "value": post
            },
        )
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Which type of post should I generate?",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Pick an item from the list:"
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                },
                "options": options,
                "action_id": action
            }
        }
    ]
    return blocks


def generate_slack_response_blocks_for_posts(
        thread_id: str,
        count: int,
        page: int,
        posts: List[Post],
        generate_more_action: str,
        post_action: str
) -> List[Any]:
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Here are your {'more ' if page > 1 else ''}{count} option(s): ",
                "emoji": True
            }
        }
    ]
    offset = (page - 1) * count
    for index, post in enumerate(posts):
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"{offset + index + 1}. {post.text}",
                    "emoji": True
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Post",
                        "emoji": True
                    },
                    "value": post.id,
                    "action_id": post_action
                }
            }
        )
    blocks.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Show More",
                    "emoji": True
                },
                "value": json.dumps({
                    'thread_id': thread_id,
                    'page': page + 1
                }),
                "action_id": generate_more_action
            }
        ]
    })
    return blocks
