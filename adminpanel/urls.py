"""
Author: Muhammed Hasan (w1689191)
Description: URLs for the custom admin panel
"""

from django.urls import path
from . import views

urlpatterns =[
    path("",views.admin_dashboard,name="admin_dashboard"),
    path("users/",views.manage_users,name="manage_users"),
    path("users/<int:user_id>/reset-password/",views.reset_user_password,name="reset_user_password"),
    path("users/<int:user_id>/toggle-active/",views.toggle_user_active,name="toggle_user_active"),
    path("users/<int:user_id>/change-role/",views.change_user_role,name="change_user_role"),
]