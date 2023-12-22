from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str = Field(None, alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
