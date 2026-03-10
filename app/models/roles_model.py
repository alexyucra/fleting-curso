from dataclasses import dataclass
from typing import Any, Optional, ClassVar
from core.base_model import BaseModel
from core.orm import ForeignKey, HasMany

@dataclass
class RolesModel(BaseModel):
    table_name: str = "roles"

    # columns
    id: Optional[int] = None
    name: Optional[str] = None
    permissions: Optional[str] = None
    created_at: Optional[Any] = None