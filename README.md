ImageKit Media Backend :

A production-ready FastAPI backend for managing social media images.
It uses PostgreSQL for persistence, ImageKit.io for image storage and delivery, and JWT authentication for security.
The project is fully Dockerized using Docker and Docker Compose for easy local development and deployment.

🚀 Features:
User Signup – Secure registration with Bcrypt password hashing

User Sign In – JWT-based authentication (OAuth2 password flow)

JWT Authentication – Protected routes using access tokens

Upload Image – Upload images to ImageKit with optional captions

Update Caption – Modify image captions

Replace Image – Replace an image while keeping the same DB record

Old image is automatically deleted from ImageKit

Delete Image – Deletes image from both PostgreSQL and ImageKit

Get User Images – Paginated list of user-uploaded images

User Profile – View user info and total uploads

🧰 Tech Stack:

Backend: FastAPI
Database: PostgreSQL
ORM: SQLAlchemy
Authentication: JWT (python-jose), Bcrypt
Image Storage: ImageKit.io
Server: Uvicorn
Containerization: Docker, Docker Compose

📁 Project Structure:


kit_backend/
│
├── app/
│   ├── main.py               # FastAPI entry point
│   ├── database.py           # DB connection setup
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── auth.py               # JWT & password logic
│   ├── dependencies.py       # DB & auth dependencies
│   └── imagekit_service.py   # ImageKit helper logic
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
└── README.md

🔑 Environment Variables:
Create a .env file in the project root

Env
# Database
DATABASE_URL=postgresql://postgres:password@db:5432/imagekit_db

# JWT
JWT_SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ImageKit
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_endpoint

🐳 Running with Docker (Recommended):
Prerequisites
Docker
Docker Compose

Build and start services:
docker compose up --build

Services started
FastAPI backend → http://localhost:9000
PostgreSQL → internal Docker network (db:5432)

Stop containers:
docker compose down

🧪 API Documentation:
Once the containers are running:
Swagger UI
👉 http://localhost:9000/docs
ReDoc
👉 http://localhost:9000/redoc

💻 Running Without Docker (Optional):
Prerequisites

Python 3.10+
PostgreSQL running locally

Install dependencies:
pip install -r requirements.txt


Start server:
uvicorn app.main:app --reload

API available at:
http://127.0.0.1:8000

🛡️ Security Notes:
.env is excluded via .gitignore
JWT secrets and ImageKit keys are never committed
Database is isolated inside Docker network
Passwords are hashed using Bcrypt

📦 Future Enhancements:
CI/CD with GitHub Actions
Role-based access control
Image analytics & metadata
AWS EC2 + RDS deployment
S3 fallback storage

👤 Author:
Abhilash
Backend Engineer | FastAPI | Docker | PostgreSQL