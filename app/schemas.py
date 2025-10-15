from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class ProductBase(BaseModel):
    name: str = Field(..., min_length = 1, max_length = 100, description = 'Product name')
    description: Optional[str] = Field(None, max_length = 500, description = 'Product description')
    price: float = Field(..., gt = 0, description = 'Product price')
    category: str = Field(..., min_length = 1, max_length = 50, description = 'Product category')
    sizes: List[str] = Field(default = [], description = 'Available Sizes')


    class ProductCreate(ProductBase):

        @field_validator('name')
        @classmethod


