from dataclasses import dataclass
from typing import Any, Optional, ClassVar
from core.base_model import BaseModel
from core.orm import ForeignKey, HasMany

@dataclass
class CategoriesModel(BaseModel):
    table_name: str = "categories"

    # columns
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[Any] = None
    posts = HasMany("posts", foreign_key="category_id")