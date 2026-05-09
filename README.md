# VideoClone Backend API

A powerful Django REST Framework backend for a YouTube-like video platform. This API provides user authentication, video upload/streaming, comments, and more.

## 🚀 Features

- **User Authentication**: Register, login, logout with token-based authentication
- **Video Management**: Upload, stream, and manage videos with thumbnails
- **Comment System**: Users can comment on videos
- **View Tracking**: Automatic view counting with duplicate prevention
- **Admin Panel**: Full Django admin interface for moderation
- **RESTful API**: Clean, documented API endpoints
- **CORS Ready**: Configured for React frontend integration
- **File Handling**: Secure video and image upload with custom storage paths

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- SQLite (default) or PostgreSQL for production
- FFmpeg (optional, for video processing)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/videoclone-backend.git
cd videoclone-backend
```

### 2. Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
# .env file
DJANGO_SECRET_KEY=your-actual-secret-key-here
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```

### 5. Apply Migrations

```bash
python manage.py makemigrations accounts
python manage.py makemigrations videos
python manage.py migrate
```

### 6. Create Cache Table (Optional, for view counting)

```bash
python manage.py createcachetable
```

### 7. Create Superuser (Admin Access)

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 8. Create Media Directories

```bash
# Windows
mkdir media\videos
mkdir media\thumbnails
mkdir media\profile_pics
mkdir static
mkdir staticfiles

# Mac/Linux
mkdir -p media/videos media/thumbnails media/profile_pics static staticfiles
```

### 9. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 📁 Project Structure

```
videoclone-backend/
├── core/                   # Main project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── accounts/              # User management app
│   ├── models.py          # Custom User model
│   ├── views.py           # Authentication views
│   ├── serializers.py     # User serializers
│   └── urls.py            # Auth endpoints
├── videos/                # Video management app
│   ├── models.py          # Video and Comment models
│   ├── views.py           # Video API views
│   ├── serializers.py     # Video serializers
│   └── urls.py            # Video endpoints
├── media/                 # User uploaded files
│   ├── videos/           # Video files
│   ├── thumbnails/       # Video thumbnails
│   └── profile_pics/     # User avatars
├── static/               # Static files
├── staticfiles/          # Collected static files
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
└── manage.py            # Django management script
```

## 🔌 API Endpoints

### Authentication Endpoints

| Method | Endpoint              | Description         | Auth Required |
| ------ | --------------------- | ------------------- | ------------- |
| POST   | `/api/auth/register/` | Register new user   | No            |
| POST   | `/api/auth/login/`    | Login user          | No            |
| POST   | `/api/auth/logout/`   | Logout user         | Yes           |
| GET    | `/api/auth/profile/`  | Get user profile    | Yes           |
| PATCH  | `/api/auth/profile/`  | Update user profile | Yes           |
| GET    | `/api/auth/csrf/`     | Get CSRF token      | No            |

### Video Endpoints

| Method | Endpoint                           | Description                 | Auth Required |
| ------ | ---------------------------------- | --------------------------- | ------------- |
| GET    | `/api/videos/`                     | List all videos (paginated) | No            |
| POST   | `/api/videos/upload/`              | Upload new video            | Yes           |
| GET    | `/api/videos/{id}/`                | Get video details           | No            |
| GET    | `/api/videos/user/{user_id}/`      | Get user's videos           | No            |
| GET    | `/api/videos/{video_id}/comments/` | Get video comments          | No            |
| POST   | `/api/videos/{video_id}/comments/` | Add comment                 | Yes           |

### Admin Endpoints

| Endpoint  | Description            |
| --------- | ---------------------- |
| `/admin/` | Django admin interface |

## 📝 Request/Response Examples

### Register User

**Request:**

```bash
POST /api/auth/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123"
}
```

**Response:**

```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "bio": "",
    "profile_picture": null,
    "subscribers_count": 0,
    "date_joined": "2024-01-01T00:00:00Z"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Login

**Request:**

```bash
POST /api/auth/login/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepass123"
}
```

**Response:**

```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Upload Video

**Request:**

```bash
POST /api/videos/upload/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: multipart/form-data

{
    "title": "My Awesome Video",
    "description": "This is a description of my video",
    "video_file": [binary data],
    "thumbnail": [binary data] (optional)
}
```

**Response:**

```json
{
  "id": 1,
  "title": "My Awesome Video",
  "description": "This is a description of my video",
  "video_file": "/media/videos/john_doe/my_awesome_video.mp4",
  "thumbnail": "/media/thumbnails/john_doe/thumbnail.jpg",
  "uploader": {
    "id": 1,
    "username": "john_doe"
  },
  "views_count": 0,
  "likes_count": 0,
  "created_at": "2024-01-01T00:00:00Z",
  "video_url": "http://localhost:8000/media/videos/john_doe/my_awesome_video.mp4",
  "thumbnail_url": "http://localhost:8000/media/thumbnails/john_doe/thumbnail.jpg"
}
```

### Get Videos Feed

**Request:**

```bash
GET /api/videos/
```

**Response:**

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/videos/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "My Awesome Video",
      "uploader": {
        "username": "john_doe"
      },
      "views_count": 150,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

## 🔧 Environment Variables Explained

| Variable               | Description                     | Default                    |
| ---------------------- | ------------------------------- | -------------------------- |
| `SECRET_KEY`           | Django secret key for security  | Required                   |
| `DEBUG`                | Enable debug mode               | True                       |
| `ALLOWED_HOSTS`        | Comma-separated list of hosts   | localhost,127.0.0.1        |
| `DB_ENGINE`            | Database engine                 | django.db.backends.sqlite3 |
| `DB_NAME`              | Database name                   | db.sqlite3                 |
| `CORS_ALLOWED_ORIGINS` | Frontend URLs for CORS          | http://localhost:3000      |
| `MAX_UPLOAD_SIZE`      | Maximum video file size (bytes) | 524288000 (500MB)          |

## 🚢 Deployment Guide

### Deploying to Production

1. **Update Settings for Production**

Create a `production.py` settings file:

```python
from .settings import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Use PostgreSQL
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
```

2. **Set Environment Variables on Server**

```bash
export SECRET_KEY='your-production-secret-key'
export DEBUG='False'
export DATABASE_URL='postgresql://user:password@localhost/dbname'
```

3. **Collect Static Files**

```bash
python manage.py collectstatic --no-input
```

4. **Use Gunicorn**

```bash
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

5. **Configure Nginx (Example)**

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /media/ {
        alias /path/to/your/media/;
    }

    location /static/ {
        alias /path/to/your/staticfiles/;
    }
}
```

## 🧪 Testing

### Run Tests

```bash
python manage.py test accounts
python manage.py test videos
```

### Test API with cURL

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123","password2":"test123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# Get videos
curl http://localhost:8000/api/videos/
```

## 🔒 Security Best Practices

1. **Never commit `.env` file to version control**
2. **Use strong SECRET_KEY in production**
3. **Enable HTTPS in production**
4. **Validate file types and sizes on server**
5. **Implement rate limiting for uploads**
6. **Use prepared statements (Django ORM does this)**
7. **Keep dependencies updated**

## 📊 Performance Optimization

1. **Use PostgreSQL for production**
2. **Implement caching for frequently accessed data**
3. **Use CDN for video streaming**
4. **Add database indexes on frequently queried fields**
5. **Implement pagination for video lists**
6. **Use selective field loading with `only()`**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django REST Framework for powerful API tools
- FFmpeg community for video processing
- All contributors and testers

## 📞 Support

For issues, questions, or contributions:

- Create an issue on GitHub
- Email: support@yourdomain.com
- Documentation: https://docs.yourdomain.com

## 🔄 Version History

- **v1.0.0** (Current)
  - Initial release
  - User authentication
  - Video upload and streaming
  - Comment system
  - View counting

---

## ⚡ Quick Start Commands

```bash
# Setup
git clone <repo-url>
cd videoclone-backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your values

# Database
python manage.py makemigrations accounts videos
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver

# The API is now running at http://localhost:8000
# Admin interface at http://localhost:8000/admin
```

---

## 📦 requirements.txt

Create a `requirements.txt` file with:

```txt
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
Pillow==10.1.0
python-dotenv==1.0.0
django-rest-framework==0.1.0
psycopg2-binary==2.9.9  # For PostgreSQL (optional)
gunicorn==21.2.0  # For production (optional)
whitenoise==6.6.0  # For static files (optional)
```

---

**Note**: This is a development setup. Always review and update security settings before deploying to production.
