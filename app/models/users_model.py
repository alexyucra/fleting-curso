from dataclasses import dataclass
from typing import Any, Optional, ClassVar
from core.base_model import BaseModel
from core.orm import ForeignKey, HasMany

@dataclass
class UsersModel(BaseModel):
    table_name: str = "users"

    # columns
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    is_active: Optional[Any] = None
    is_verified: Optional[Any] = None
    role_id: Optional[int] = None
    created_at: Optional[Any] = None
    updated_at: Optional[Any] = None
    last_login_at: Optional[Any] = None
    posts = HasMany("posts", foreign_key="user_id")
    comments = HasMany("comments", foreign_key="user_id")