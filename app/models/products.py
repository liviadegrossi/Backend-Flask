from pydantic import BaseModel
from typing import Optional # attributes can be optional

class Product(BaseModel):
    '''
    Data model for a product. Name, price and stock are mandatory attibutes
    '''
    name: str 
    price: float 
    description: Optional[str] = None
    stock: int 
    sku: str # Stock Keeping Unit