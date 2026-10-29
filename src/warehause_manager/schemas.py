from pydantic import BaseModel, Field, ConfigDict

class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    quantity: int = Field(ge=0, default=0)
    comment: str | None = Field(default=None)

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    quantity: int | None = Field(default=None, ge=0)
    comment: str | None = None

class ProductRead(BaseModel):
    id: int
    name: str = Field(min_length=1)
    quantity: int = Field(ge=0)
    comment: str | None = None

    model_config = ConfigDict(from_attributes=True)

class ProductStock(BaseModel):
    change: int
