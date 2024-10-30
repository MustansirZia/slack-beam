from hashlib import md5
from typing import List, Optional

from sqlalchemy.orm import Session

from app.storage.engines.sqlite import engine
from app.storage.models import Base
from app.storage.models.post import PostType, Post

Base.metadata.create_all(engine)


def save_raw_posts(raw_posts: List[str], post_type: PostType) -> List[Post]:
    posts: List[Post] = []
    for raw_post in raw_posts:
        post = Post()
        post.id = md5(raw_post.encode()).hexdigest()
        post.text = raw_post
        post.type = post_type.value
        posts.append(post)

    with Session(engine, expire_on_commit=False) as session:
        existing_post_ids = {
            existing_post.id for existing_post in
            session.query(Post, Post.id)
            .filter(Post.id.in_([
                post.id for post in posts
            ]))
            .all()
        }

        for post in posts:
            if post.id in existing_post_ids:
                # Post already present in storage, so we can skip.
                continue
            session.add(post)

        session.commit()

    return posts


def get_post_by_id(post_id: str) -> Optional[Post]:
    with Session(engine) as session:
        return session.get(Post, post_id)
