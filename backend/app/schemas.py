from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class HtmlCodeUpload(BaseModel):
    html_content: str
    title: Optional[str] = None

class PageResponse(BaseModel):
    id: str
    title: Optional[str] = None
    url: str # This will be constructed on the fly
    created_at: datetime
    view_count: int
    is_active: bool

    class Config:
        from_attributes = True # For SQLAlchemy ORM compatibility

class PageUpdate(BaseModel):
    title: Optional[str] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
