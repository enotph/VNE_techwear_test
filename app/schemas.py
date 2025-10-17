from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class ProductBase(BaseModel):
    name: str = Field(..., min_length = 1, max_length = 100, description = 'Product name')
    description: Optional[str] = Field(None, max_length = 500, description = 'Product description')
    price: float = Field(..., gt = 0, description = 'Product price')
    category: str = Field(..., min_length = 1, max_length = 50, description = 'Product category')
    sizes: List[str] = Field(default = [], description = 'Available Sizes')


class ProductCreate(ProductBase):                                  #схема валидации name

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Product name cannot be empty')
        return v.strip()


class ProductUpdate(BaseModel):                                     #схема для обновления данных продукта

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    sizes: Optional[List[str]] = None


class ProductResponse(ProductBase):                                 #модель для сериализации
    id: int

    class Config:
        from_attributes = True

