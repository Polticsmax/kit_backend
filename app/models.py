from sqlalchemy import Column , Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime 

class USER(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


    images = relationship("IMAGE", back_populates="owner")


class IMAGE(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_url = Column(String, nullable=False)
    imagekit_file_id = Column(String, nullable=False)
    caption= Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("USER", back_populates="images")

    
