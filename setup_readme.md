# SkyEngineering Portal

Group project built with **Django**.

This repository contains the source code for the **SkyEngineering Portal system**. The project is developed collaboratively using **Git and GitHub**.

---

# Team Workflow Guide

To avoid breaking each other's code, **no one should work directly on the ****`main`**** branch**.

All development must be done in **feature branches** and merged through **Pull Requests**.

---

# 1. First Time Setup (Clone the Project)

Each team member should clone the repository:

```
git clone https://github.com/jolenjolen/portal-skyengineering.git
```

Move into the project folder:

```
cd portal-skyengineering
```

Activate your virtual environment if required.

---

# 2. Always Get Latest Code First

Before starting work each day, update your local project:

```
git checkout main
git pull origin main
```

This ensures you are working with the **latest version** of the project.

---

# 3. Create Your Own Branch

Never work directly on `main`.

Create a branch for your feature:

```
git checkout -b feature-name
```

Example:

```
git checkout -b login-system
```

---

# 4. Do Your Work

Example tasks:

Create apps:

```
python manage.py startapp accounts
```

Edit models, views, templates, etc.

---

# 5. Save Your Changes

Stage your changes:

```
git add .
```

Commit your work:

```
git commit -m "Describe what you changed"
```

Example:

```
git commit -m "Added accounts app and login view"
```

---

# 6. Push Your Branch to GitHub

```
git push origin feature-name
```

Example:

```
git push origin login-system
```

---

# 7. Create a Pull Request

After pushing your branch:

1. Go to the GitHub repository.
2. Click **Compare & Pull Request**.
3. Select:

```
feature-name → main
```

4. Add a description of what you changed.
5. Submit the Pull Request.

---

# 8. Code Review and Merge

Other team members should review the code.

If everything looks good, the Pull Request can be **merged into ****`main`**.

---

# 9. After a Merge

After someone merges a feature:

Update your local project again before continuing work:

```
git checkout main
git pull origin main
```

Then create a **new branch for your next task**.

---

# Suggested Branch Naming

Use clear branch names:

```
auth-system
student-dashboard
admin-panel
database-models
api-endpoints
frontend-ui
```

---

# Useful Git Commands

Check current branch:

```
git branch
```

Switch branch:

```
git checkout branch-name
```

Check changes:

```
git status
```

---

# Important Rules

1. **Do not push directly to ****`main`****.**
2. Always work on your **own branch**.
3. Always **pull latest code before starting work**.
4. Use **Pull Requests for merging code**.
5. Write clear commit messages.

---

# Project Structure

```
portal-skyengineering/
│
├── manage.py
├── README.md
│
└── skyengineering/
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

Apps will be added as development continues.

---

# Development Stack

* Python
* Django
* Git
* GitHub

---

# Contributors

SkyEngineering Development Team 
