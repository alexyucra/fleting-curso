from dataclasses import dataclass
from typing import Any, Optional, ClassVar
from core.base_model import BaseModel
from core.orm import ForeignKey, HasMany

@dataclass
class CommentsModel(BaseModel):
    table_name: str = "comments"

    # columns
    id: Optional[int] = None
    post_id: Optional[int] = None
    user_id: Optional[int] = None
    author_name: Optional[str] = None
    author_email: Optional[str] = None
    content: Optional[str] = None
    is_approved: Optional[Any] = None
    created_at: Optional[Any] = None

    # relations (ForeignKey)
    user = ForeignKey("users", local="user_id", remote="id")
    post = ForeignKey("posts", local="post_id", remote="id")