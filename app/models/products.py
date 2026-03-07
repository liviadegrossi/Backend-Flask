from pydantic import BaseModel
from typing import Optional # attributes can be optional

# Guarantees a product has all mandatory data
class Product(BaseModel):
    name: str # mandatory
    price: float # mandatory
    description: Optional[str] = None
    stock: int # mandatory