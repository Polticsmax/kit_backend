from imagekitio import ImageKit
from dotenv import load_dotenv
import os
import base64
import uuid

load_dotenv()

# init
imagekit = ImageKit(private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"))

# upload
def upload_image(file_bytes: bytes, filename: str):
    unique_filename = f"{uuid.uuid4()}_{filename}"
    #encoded_file = base64.b64encode(file_bytes).decode("utf-8")

    result = imagekit.files.upload(
        file=file_bytes,
        file_name=unique_filename,
    )

    return {"url": result.url, "file_id": result.file_id}

# delete
def delete_image(file_id: str):
    imagekit.files.delete(file_id)
