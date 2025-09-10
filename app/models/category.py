from pydantic import BaseModel

class Category(BaseModel):
    name: str
    type: str
    active: bool