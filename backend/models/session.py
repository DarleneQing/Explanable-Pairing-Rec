from pydantic import BaseModel
from datetime import datetime

class Session(BaseModel):
    session_id: str
    created_at: datetime
    is_active: bool
    name: str = ''
    section: str = ''
    garment_group: str = ''
    product_type: str = ''
    color: str = ''
    graphic_appearance: str = ''
