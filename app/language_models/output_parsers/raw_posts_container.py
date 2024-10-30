from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List


class RawPostsContainer(BaseModel):
    """A container that contains an array of raw social media posts."""

    posts: List[str] = Field(description="an array of social media posts")
