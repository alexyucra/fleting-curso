from dataclasses import dataclass
from typing import Any, Optional, ClassVar
from core.base_model import BaseModel
from core.orm import ForeignKey, HasMany

@dataclass
class PostsModel(BaseModel):
    table_name: str = "posts"

    # columns
    id: Optional[int] = None
    user_id: Optional[int] = None
    category_id: Optional[int] = None
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    status: Optional[str] = None
    view_count: Optional[int] = None
    published_at: Optional[Any] = None
    created_at: Optional[Any] = None
    updated_at: Optional[Any] = None

    # relations (ForeignKey)
    categorie = ForeignKey("categories", local="category_id", remote="id")
    user = ForeignKey("users", local="user_id", remote="id")
    comments = HasMany("comments", foreign_key="post_id")