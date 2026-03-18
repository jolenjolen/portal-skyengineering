# Sky Engineering Portal

## 📌 Overview

Sky Engineering Portal is a web-based platform designed for engineers to:

* Log in securely
* View teams and departments
* Access staff directory
* Communicate via messaging
* Collaborate across the organization

---

## 🏗️ Project Structure

```
skyengineering/
├── manage.py
├── portal/          # Main project configuration (settings, URLs)
├── accounts/        # Authentication (login, signup)
├── teams/           # Teams and departments
├── people/          # Staff profiles and directory
├── messaging/       # Messaging system
├── static/          # Global static files (CSS, JS)
├── media/           # User-uploaded files
```

---

## 🧠 Architecture

* **Django Project (`portal`)**

  * Handles configuration and routing
* **Django Apps**

  * Each app represents a feature/module
  * Apps are reusable and modular

---

## 🗄️ Database

* Managed via Django ORM
* Configured in `portal/settings.py`
* Default: SQLite (`db.sqlite3` in root directory)
* Can be replaced with PostgreSQL/MySQL for production

---

## 🚀 Setup Instructions

### 1. Clone repository

```
git clone <repo-url>
cd skyengineering
```

### 2. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run migrations

```
python3 manage.py migrate
```

### 5. Start development server

```
python3 manage.py runserver
```

---

## 🌐 Routes (Planned)

* `/login/` → User login
* `/signup/` → User registration
* `/teams/` → Team overview
* `/people/` → Staff directory
* `/messages/` → Messaging system

---

## 📁 Static & Media Files

* Static files (CSS, JS):
  `static/` or `app/static/app_name/`

* Uploaded media:
  `media/`

---

## 🧩 Development Guidelines

* Each feature must be developed in its own app
* Keep views thin, use models for logic
* Follow Django naming conventions
* Use templates inside:

  ```
  app/templates/app_name/
  ```

---

## 👥 Team Notes

* Do not modify `portal/settings.py` without discussion
* Keep commits small and descriptive
* Use branches for features

---

## 🔮 Future Features

* Real-time messaging (WebSockets)
* Notifications system
* Role-based access control
* Dashboard analytics

---
