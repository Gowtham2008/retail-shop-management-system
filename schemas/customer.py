from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(min_length=10, max_length=15)
    email: str | None = None
    address: str | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str | None
    address: str | None

    class Config:
        from_attributes = True