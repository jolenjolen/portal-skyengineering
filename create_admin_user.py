"""
Author: Muhammed Hasan (w1689191)
Description: Creates a default admin user for testing/admin access
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE","portal.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from core.models import TblUser

def create_admin_user():
    admin_user,created = TblUser.objects.get_or_create(
        uname="admin",
        defaults={
            "fname": "SKY",
            "sname": "Admin",
            "email": "admin@sky.com",
            "password": make_password("Admin123"),
            "role": "Admin",
            "created": timezone.now(),
            "active": True,
        }

    )

    if created:
        print("Admin User has successfully been created.")
    else:
        print("Admin user already exists.")

create_admin_user()