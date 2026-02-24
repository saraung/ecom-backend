from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserProfileBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    phone_number: str

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True