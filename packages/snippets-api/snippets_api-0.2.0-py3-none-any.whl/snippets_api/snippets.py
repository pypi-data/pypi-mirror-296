from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field


class RedditSubmissionComment(BaseModel):
    id: str
    url: str
    body: str


class RedditSubmission(BaseModel):
    type: Literal["reddit"] = Field(default="reddit")
    id: str
    url: str
    title: str
    subreddit: str
    comments: List[RedditSubmissionComment]


Snippet = Union[RedditSubmission]
