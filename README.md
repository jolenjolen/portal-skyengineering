# SKY Engineering Portal

An internal engineering portal built with **Django** for managing teams, departments, projects, dependencies, messaging, scheduling, and reporting.

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/jolenjolen/portal-skyengineering.git
cd portal-skyengineering
```

### 2. Install Dependencies

Make sure you have Python 3.10+ installed, then install the required packages:

```bash
pip install django
```

Or if a `requirements.txt` is present:

```bash
pip install -r requirements.txt
```

### 3. Run the Development Server

```bash
py manage.py runserver
```

Then open your browser and go to:

```
http://127.0.0.1:8000/
```

---

## Logging In

### Admin Account

Use the following credentials to log in as an administrator:

```
Username: admin
Password: Admin123
```

The admin account has full access to the portal including the admin dashboard, where you can manage users, teams, departments, projects, and dependencies.

### Standard User Account

To test the portal as a standard user, browse the user list in the admin dashboard and pick any user. All standard user accounts use the default password:

```
Password: Password123
```

If a user's password is not working, you can reset it from the admin dashboard:

1. Log in as admin
2. Go to **Admin → Manage Users**
3. Find the user and click **Reset Password**
4. Their password will be reset to `Password123`
5. Log out and log back in as that user

### Creating a New User

Alternatively, you can create a fresh user to test with:

1. Log in as admin
2. Go to **Admin → Manage Users**
3. Click **Add New User** and fill in the details
4. A one-time generated password will be displayed — copy it
5. Log out and log in with the new username and that password

---

## Django Admin Panel (Raw Database Access)

A Django superuser is available for direct database access via the built-in Django admin interface:

```
URL:      http://127.0.0.1:8000/admin/
Username: admin
Password: Admin123
```

This gives access to all raw database tables including users, teams, departments, projects, dependencies, messages, and audit logs.

---

## Project Structure

```
portal-skyengineering/
│
├── manage.py
├── README.md
├── db.sqlite3
│
├── portal/                  # Project config (settings, urls)
│   ├── settings.py
│   └── urls.py
│
├── core/                    # Shared models used by all apps
│   └── models.py
│
├── accounts/                # Login, logout, contact, help, pp, tos
│   ├── views.py
│   ├── urls.py
│   └── templates/accounts/
│
├── adminpanel/              # Admin dashboard and CRUD management
│   ├── views.py
│   ├── urls.py
│   └── templates/adminpanel/
│
├── dashboard/               # Main homepage/dashboard
│   └── templates/dashboard/
│
├── reports/                 # Reports and data visualisation
│   ├── views.py
│   └── templates/reports/
│
├── messaging/               # Internal messaging system
│   ├── models.py
│   ├── views.py
│   └── templates/messaging/
│
├── organisation/            # Organisation overview and departments
│   └── templates/organisation/
│
└── static/                  # Global static files (CSS, images)
    ├── css/
    └── media/
```

---

## Team Workflow (For Contributors)

> Full workflow guide is in `setup_readme.md`

- **Never push directly to `main`**
- Always create a feature branch: `git checkout -b feature-name`
- Push your branch and open a **Pull Request** on GitHub
- Only merge after review and no conflicts

```bash
# Daily start routine
git checkout main
git pull origin main
git checkout -b your-feature-name
```

---

## Tech Stack

- Python 3
- Django 6
- SQLite
- Bootstrap 5
- Chart.js
- Git & GitHub
