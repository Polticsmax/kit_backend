from pydantic import BaseModel , EmailStr
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    email : EmailStr
    password : str


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class TokenResponse(BaseModel):
    access_token : str
    token_type : str = "bearer"


class UserResponse(BaseModel):
   id : int
   email : EmailStr
  

   class Config:
       from_attributes = True


class ImageCreateResponse(BaseModel):
    image_url : str
    imagekit_file_id : str
    caption : str | None

    class Config:
        from_attributes = True


class ImageCaptionUpdate(BaseModel):
    caption : str | None = None



class ImageResponse(BaseModel):
    id: int
    image_url: str
    caption: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ImageListResponse(BaseModel):
    images: List[ImageResponse]
    total: int
    page: int
    limit: int


class ProfileResponse(BaseModel):
    user_id: int
    email: EmailStr
    total_images: int