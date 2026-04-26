"""
Author: Muhammed Hasan (w1689191)
"""

from django.shortcuts import render, redirect
from accounts.views import is_admin
from core.models import TblUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages


# admin dashboard
def admin_dashboard(request):
    if not is_admin(request):
        return redirect("home")
    context = {
        "is_admin_user": is_admin(request),
    }
    return render(request, "adminpanel/dashboard.html", context)


# manage users
def manage_users(request):
    if not is_admin(request):
        return redirect("home")

    users = TblUser.objects.all()

    context = {
        "users": users,
    }

    return render(request, "adminpanel/manage_users.html", context)


# reset a users password to default
def reset_user_password(request, user_id):
    if not is_admin(request):
        return redirect("home")

    if request.method == "POST":
        user = TblUser.objects.get(id=user_id)
        #stop admins from resetting own password in manage users
        if user.id == request.session.get("user_id"):
            return redirect("manage_users")
        user.password = make_password("Password123")
        user.save(update_fields=["password"])
    return redirect("manage_users")
