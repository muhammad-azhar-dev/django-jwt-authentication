# Django JWT Authentication API

A complete JWT authentication system built using Django and Django Rest Framework (DRF). This project includes user registration, login, password change, and password reset via email.

## Features
- User Registration
- User Login with JWT Authentication
- Change Password
- Reset Password via Email
- Secure API with JWT (Access & Refresh Tokens)
- CORS support for frontend integration

## Technologies Used
- Django
- Django REST Framework (DRF)
- djangorestframework-simplejwt (JWT Authentication)
- django-cors-headers (CORS Handling)
- django-dotenv (Environment Variables)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/muhammad-azhar9920/django-jwt-authentication.git
cd django_auth
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add the following:
```ini
EMAIL_USER = your_email_address
EMAIL_PASS = your_app_password
EMAIL_FROM = your_email_address
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

## API Endpoints

| Method | Endpoint                | Description                 |
|--------|-------------------------|-----------------------------|
| POST   | `/api/user/register`        | Register a new user         |
| POST   | `/api/user/login`           | Obtain JWT tokens           |
| POST   | `/api/user/changepassword` | Change user password        |
| POST   | `/api/user/send-reset-password-email`  | Request password reset link |
| POST   | `/api/user/reset-password/id/token/`   | Confirm password reset with user id and token      |

## JWT Authentication Usage

After successful login, you will receive an `access` and `refresh` token.

Use the `access` token for authenticated requests:
```http
Authorization: Bearer your-access-token
```

To refresh the token:
```bash
POST /api/token/refresh/
{
  "refresh": "your-refresh-token"
}
```

## CORS Configuration
If you are integrating with a frontend, update `settings.py` to allow CORS:
```python
INSTALLED_APPS = [
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React or frontend URL
]
```

## Contributing
Feel free to fork this repository and submit a pull request with improvements.

## License
This project is licensed under the MIT License.

---

⭐ Don't forget to star this repository if you find it helpful!


