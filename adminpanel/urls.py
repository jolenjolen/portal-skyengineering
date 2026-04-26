"""
Author: Muhammed Hasan (w1689191)
Description: URLs for the custom admin panel
"""

from django.urls import path
from . import views

urlpatterns =[
    path("",views.admin_dashboard,name="admin_dashboard"),
    path("users/",views.manage_users,name="manage_users"),
    path("users/<int:user_id>/reset-password",views.reset_user_password,name="reset_user_password")
]