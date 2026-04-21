# 🚀 Scalable Backend API with Authentication & Role-Based Access

## 📌 Overview

This project is a scalable backend API built using **FastAPI**, implementing authentication, and CRUD operations. A simple frontend can be integrated to interact with the APIs.

---

## ⚙️ Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL via SQLAlchemy ORM
* **Authentication:** JWT (JSON Web Tokens)
* **Language:** Python

---

## 🔑 Features

### ✅ Authentication

* User Registration
* User Login with JWT
* Password hashing (secure storage)


### ✅ CRUD Operations (Posts)

* Create Post
* Get All Posts (with pagination)
* Get Single Post
* Update Post (owner only)
* Delete Post (owner only)
---

## 📂 Project Structure

```
project/
│
├── router/
│   ├── auth.py
│   ├── post.py
│   ├── user.py
│   └── vote.py
│
├── config.py
├── database.py
├── main.py
├── models.py
├── oauth2.py
├── schemas.py
├── utils.py
│
├── .env
├── .gitignore
```

---

## 🔌 API Endpoints

### 🔐 Auth

* `POST /api/v1/auth/login`

### 👤 Users

* `POST /api/v1/users` → Register user
* `GET /api/v1/users/{id}` → Get user

### 📝 Posts

* `POST /api/v1/posts` → Create post
* `GET /api/v1/posts` → Get all posts
* `GET /api/v1/posts/{id}` → Get single post
* `PUT /api/v1/posts/{id}` → Update post
* `DELETE /api/v1/posts/{id}` → Delete post

---

## 🔒 Security Features

* Password hashing using bcrypt
* JWT-based authentication
* Protected routes with dependency injection
* Input validation using Pydantic

---

## 📊 Pagination

Supports query parameters:

```
GET /api/v1/posts?limit=10&skip=0
```

---

## 📘 API Documentation

Swagger UI available at:

```
http://localhost:8000/docs
```

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/roshanmishra17/social_media_backend.git
cd project
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` file:

```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the server

```
uvicorn main:app --reload
```


---

## 👨‍💻 Author

Roshan Mishra

---
=
