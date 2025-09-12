from pydantic import BaseModel
from datetime import datetime

class Sale(BaseModel):
    sale_date: datetime
    product_id: str
    quantity: int
    total_value: float