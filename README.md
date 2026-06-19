# 📝 Django Blog CMS

<div align="center">

![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.15-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Swagger](https://img.shields.io/badge/Docs-Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A **production-ready Blog & CMS REST API** built with Django 5, Django REST Framework, JWT authentication, threaded comments, full-text search, and auto-generated Swagger docs.

[Features](#-features) • [Tech Stack](#-tech-stack) • [Getting Started](#-getting-started) • [API Docs](#-api-documentation) • [Project Structure](#-project-structure) • [Running Tests](#-running-tests)

</div>

---

## ✨ Features

- 🔐 **JWT Authentication** — Register, login, refresh & blacklist tokens (logout)
- 👤 **Custom User Model** — Extended with bio, avatar, website, and post count
- 📄 **Blog Posts** — Full CRUD with draft/published status, auto-slug, auto read time
- 🏷️ **Tags** — Many-to-many tagging system with post count per tag
- 💬 **Threaded Comments** — Top-level comments and nested replies with approval system
- 🔍 **Full-Text Search** — Search posts by title, content, author, or tag
- 🎛️ **Advanced Filtering** — Filter by status, author, tag, date range
- 📊 **View Counter** — Track post views on every retrieve
- 🛡️ **Permission System** — Author-only write access with custom `IsAuthorOrReadOnly` permission
- 🐳 **Docker Ready** — Full stack with one command
- 🧑‍💼 **Django Admin** — Fully configured admin panel for all models
- 📄 **Swagger UI** — Auto-generated via drf-spectacular
- 🧪 **Test Suite** — 20+ tests across accounts, blog, and comments

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5.0 + Django REST Framework |
| Language | Python 3.12 |
| Database | PostgreSQL 16 |
| ORM | Django ORM |
| Migrations | Django Migrations |
| Auth | JWT (SimpleJWT) with token blacklisting |
| Filtering | django-filter |
| API Docs | drf-spectacular (Swagger + ReDoc) |
| Image Handling | Pillow |
| Testing | Pytest + pytest-django |
| Containerization | Docker + Docker Compose |

---

## 🚀 Getting Started

### Prerequisites

- [Docker & Docker Compose](https://docs.docker.com/get-docker/) *(recommended)*
- Or Python 3.12+ and PostgreSQL installed locally

---

### ▶ Option 1: Run with Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/rchintan405/django-blog-cms.git
cd django-blog-cms

# 2. Set up environment variables
cp .env.example .env
# Edit .env and set a strong DJANGO_SECRET_KEY

# 3. Start the full stack (runs migrations automatically)
docker compose up --build

# API is live at http://localhost:8000
# Swagger UI at http://localhost:8000/docs
# Django Admin at http://localhost:8000/admin
```

---

### ▶ Option 2: Run Locally

```bash
# 1. Clone and enter the project
git clone https://github.com/rchintan405/django-blog-cms.git
cd django-blog-cms

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Update DATABASE_URL to your local PostgreSQL connection

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser (for Django Admin)
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver

# API is live at http://localhost:8000
```

---

## 📖 API Documentation

| Doc Type | URL |
|---|---|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Django Admin | http://localhost:8000/admin |

---

### 🔑 Auth Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/v1/auth/register/` | Register new user + receive tokens | ❌ |
| `POST` | `/api/v1/auth/login/` | Login and receive JWT tokens | ❌ |
| `POST` | `/api/v1/auth/token/refresh/` | Refresh access token | ❌ |
| `POST` | `/api/v1/auth/logout/` | Blacklist refresh token | ✅ |
| `GET/PATCH` | `/api/v1/auth/me/` | Get or update own profile | ✅ |
| `GET` | `/api/v1/auth/users/<username>/` | Public profile by username | ❌ |

---

### 📄 Post Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/api/v1/posts/` | List published posts | ❌ |
| `POST` | `/api/v1/posts/create/` | Create a new post | ✅ |
| `GET` | `/api/v1/posts/me/` | My posts (all statuses) | ✅ |
| `GET` | `/api/v1/posts/<slug>/` | Post detail (increments views) | ❌ |
| `PATCH` | `/api/v1/posts/<slug>/` | Update own post | ✅ |
| `DELETE` | `/api/v1/posts/<slug>/` | Delete own post | ✅ |

#### Query Parameters

```
GET /api/v1/posts/?search=django&tag=python&author=johndoe&ordering=-views
GET /api/v1/posts/?published_after=2025-01-01&published_before=2025-12-31
```

---

### 🏷️ Tag Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/api/v1/tags/` | List all tags | ❌ |
| `POST` | `/api/v1/tags/` | Create a tag | ✅ |
| `GET/PATCH/DELETE` | `/api/v1/tags/<slug>/` | Manage tag | Admin |

---

### 💬 Comment Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/api/v1/posts/<slug>/comments/` | List approved comments | ❌ |
| `POST` | `/api/v1/posts/<slug>/comments/` | Add a comment or reply | ✅ |
| `GET/PATCH/DELETE` | `/api/v1/comments/<id>/` | Manage own comment | ✅ |

#### Example: Threaded Comment Response

```json
{
  "id": 1,
  "author": { "id": 2, "username": "johndoe" },
  "body": "Great article!",
  "reply_count": 1,
  "replies": [
    {
      "id": 2,
      "author": { "id": 3, "username": "janedoe" },
      "body": "Totally agree!",
      "created_at": "2025-07-02T10:00:00Z"
    }
  ],
  "created_at": "2025-07-01T12:00:00Z"
}
```

---

## 📁 Project Structure

```
django-blog-cms/
├── apps/
│   ├── accounts/              # Custom user model, auth views
│   │   ├── models.py          # Extended AbstractUser
│   │   ├── serializers.py     # Register, profile, update
│   │   ├── views.py           # Register, me, logout, public profile
│   │   ├── urls.py
│   │   └── admin.py
│   ├── blog/                  # Posts and tags
│   │   ├── models.py          # Post (auto-slug, read-time), Tag
│   │   ├── serializers.py     # List, detail, create/update
│   │   ├── views.py           # CRUD + search + filtering
│   │   ├── filters.py         # PostFilter (django-filter)
│   │   ├── permissions.py     # IsAuthorOrReadOnly
│   │   ├── urls.py
│   │   └── admin.py
│   └── comments/              # Threaded comments
│       ├── models.py          # Comment with parent FK (replies)
│       ├── serializers.py     # Comment + Reply
│       ├── views.py
│       ├── urls.py
│       └── admin.py
├── config/
│   ├── settings.py            # All Django + DRF + JWT settings
│   ├── urls.py                # Root URL config + Swagger
│   └── wsgi.py
├── tests/
│   ├── conftest.py            # Shared fixtures (users, posts, comments)
│   ├── test_accounts.py       # 7 auth tests
│   ├── test_blog.py           # 13 post/tag tests
│   └── test_comments.py       # 6 comment tests
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── .env.example
```

---

## 🧪 Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov=apps --cov-report=term-missing

# Run specific test file
pytest tests/test_blog.py -v
```

---

## 🔒 Security Notes

- Passwords hashed via Django's built-in PBKDF2
- JWT tokens signed and expire in 30 minutes (configurable)
- Refresh tokens are **blacklisted on logout** — can't be reused
- Object-level permissions: only the post/comment author can edit or delete
- `.env` is gitignored — use `.env.example` as a template

---

## 🤝 Contributing

Pull requests are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to branch: `git push origin feat/your-feature`
5. Open a Pull Request

> **Note:** Direct pushes to `main` and `develop` are branch-protected. All changes must go through a reviewed PR.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ by [Karan Prajapati](https://kretoss.com/portfolio)

[![Portfolio](https://img.shields.io/badge/Portfolio-kretoss.com-blue?style=flat-square)](https://kretoss.com/portfolio)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://linkedin.com/in/your-profile)
[![Upwork](https://img.shields.io/badge/Upwork-Hire%20Me-6FDA44?style=flat-square&logo=upwork&logoColor=white)](https://www.upwork.com/freelancers/your-profile)

</div>
