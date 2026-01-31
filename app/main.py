from fastapi import FastAPI , Depends , HTTPException , status, File , UploadFile, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import engine
from app import models
from app.schemas import UserCreate , UserLogin , TokenResponse
from app.dependencies import get_db
from app.auth import create_access_token , verify_password , hash_password

from app.dependencies import get_current_user
from app.schemas import UserResponse, ImageCreateResponse , ImageCaptionUpdate , ImageResponse , ImageListResponse , ProfileResponse

from app.imagekit_service import upload_image , delete_image


MAX_FILE_SIZE = 5 * 1024 * 1024  # maximum image upload size
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]

app = FastAPI(title="Imagekit Media Backend")

models.Base.metadata.create_all(bind=engine)


@app.post("/signup", response_model=TokenResponse)
def signup(user: UserCreate , db: Session= Depends(get_db)):
    existing_user = db.query(models.USER).filter(models.USER.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "Email already registered")
    
    new_user = models.USER(
        email=user.email ,
        hashed_password=hash_password(user.password)

    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"sub": str(new_user.id)})


    return {"access_token":token}


@app.post("/login" , response_model=TokenResponse)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.USER).filter(models.USER.email == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid email or password")
    
    token = create_access_token(data={"sub":str(db_user.id)})

    return {"access_token":token}



@app.get("/me", response_model=UserResponse)
def read_current_user(current_user: models.USER = Depends(get_current_user)):
    return current_user


@app.post("/images", response_model =ImageCreateResponse)
def upload_user_image(
    caption: str | None = Form(None),
    file : UploadFile = File(...),
    db: Session =Depends(get_db),
    current_user : models.USER = Depends(get_current_user),
):

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only JPEG and PNG images are allowed"
        )

    file_bytes = file.file.read()

    if len(file_bytes) > MAX_FILE_SIZE:
       raise HTTPException(
             status_code=400,
             detail="File size exceeds 5 MB limit"
    )

    imagekit = upload_image(
        file_bytes=file_bytes,
        filename=file.filename
 )
    

    new_image = models.IMAGE(
        user_id=current_user.id,
        image_url=imagekit["url"],
        imagekit_file_id=imagekit["file_id"],
        caption=caption
    )

    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return new_image


@app.put("/images/{image_id}" , response_model=ImageResponse)
def update_image_caption(
    image_id: int,
    data: ImageCaptionUpdate,
    db: Session = Depends(get_db),
    current_user: models.USER = Depends(get_current_user)
):
    image = db.query(models.IMAGE).filter(models.IMAGE.id == image_id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    if image.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    image.caption = data.caption
    db.commit()
    db.refresh(image)

    return image


@app.put("/images/{image_id}/replace" , response_model=ImageResponse)
def replace_image(
    image_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.USER = Depends(get_current_user)
):
    image = db.query(models.IMAGE).filter(models.IMAGE.id == image_id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    if image.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only JPEG and PNG images are allowed"
        )

    delete_image(image.imagekit_file_id)

    file_bytes = file.file.read()
    imagekit_result = upload_image(file_bytes, file.filename)

    image.image_url = imagekit_result["url"]
    image.imagekit_file_id = imagekit_result["file_id"]

    db.commit()
    db.refresh(image)

    return image


@app.delete("/images/{image_id}")
def delete_user_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: models.USER = Depends(get_current_user)
):
    image = db.query(models.IMAGE).filter(models.IMAGE.id == image_id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    if image.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    delete_image(image.imagekit_file_id)
    db.delete(image)
    db.commit()

    return {"message": "Image deleted successfully"}


@app.get("/images", response_model=ImageListResponse)
def get_my_images(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.USER = Depends(get_current_user)
):
    offset = (page - 1) * limit

    total = db.query(models.IMAGE).filter(
        models.IMAGE.user_id == current_user.id
    ).count()

    images = db.query(models.IMAGE).filter(
        models.IMAGE.user_id == current_user.id
    ).offset(offset).limit(limit).all()

    return {
        "images": images,
        "total": total,
        "page": page,
        "limit": limit
    }


@app.get("/profile",response_model=ProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: models.USER = Depends(get_current_user)
):
    image_count = db.query(models.IMAGE).filter(
        models.IMAGE.user_id == current_user.id
    ).count()

    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "total_images": image_count
    }