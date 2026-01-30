# ImageKit Media Backend

A robust FastAPI backend application designed to handle social media images. It uses **PostgreSQL** for data persistence and **ImageKit.io** for efficient image storage and delivery. The application features secure JWT authentication and a full suite of image management capabilities.

## Features

1.  **User Signup**: Register new users with secure password hashing (Bcrypt).
2.  **User Sign In**: Authenticate users and issue JWT access tokens.
3.  **JWT Authentication**: Secure endpoints using OAuth2 (Password flow).
4.  **Upload Image**: Upload images to ImageKit.io with optional captions.
5.  **Update Caption**: Modify the caption of an existing image.
6.  **Replace Image**: Fully replace an existing image file while maintaining the database record (automatically deletes the old image from ImageKit).
7.  **Delete Image**: Remove images from both the database and ImageKit storage.
8.  **Get User Images**: Retrieve a paginated list of images uploaded by the authenticated user.
9.  **User Profile**: View user profile details including email, user ID, and total upload count.

## Tech Stack

*   **Framework**: FastAPI
*   **Database**: PostgreSQL
*   **ORM**: SQLAlchemy
*   **Storage**: ImageKit.io
*   **Authentication**: Python-Jose (JWT), Bcrypt
*   **Server**: Uvicorn

## Prerequisites

*   Python 3.10+
*   PostgreSQL installed and running.
*   An [ImageKit.io](https://imagekit.io/) account.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd kit_backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] python-dotenv imagekitio bcrypt python-multipart
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root directory and add the following configurations:

    ```env
    # Database Configuration
    DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>

    # Security
    JWT_SECRET_KEY=your_super_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60

    # ImageKit Configuration
    IMAGEKIT_PUBLIC_KEY=your_public_key_here
    IMAGEKIT_PRIVATE_KEY=your_private_key_here
    IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_url_endpoint
    ```

5.  **Database Setup:**
    *   Create a database in PostgreSQL (e.g., `imagekit_db`).
    *   The application will automatically create the necessary tables (`users`, `images`) when you run it for the first time.

## Running the Application

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

FastAPI provides interactive API documentation automatically. Once the server is running, visit:

*   **Swagger UI**: http://127.0.0.1:8000/docs - Test endpoints directly in the browser.
*   **ReDoc**: http://127.0.0.1:8000/redoc - Alternative documentation view.

## Project Structure

*   `app/main.py`: Application entry point and route definitions.
*   `app/models.py`: SQLAlchemy database models (`USER`, `IMAGE`).
*   `app/schemas.py`: Pydantic models for request/response validation.
*   `app/auth.py`: Logic for password hashing and JWT token creation.
*   `app/dependencies.py`: Dependency injection for database sessions and current user retrieval.
*   `app/imagekit_service.py`: Helper functions to interact with the ImageKit SDK.
*   `app/database.py`: Database connection setup.
