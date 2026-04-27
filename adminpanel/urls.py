"""
Author: Muhammed Hasan (w1689191), Jolen Mascarenhas (w2078969)
Description: URLs for the custom admin panel
"""

from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path("", views.admin_dashboard, name="admin_dashboard"),

    # ─── Users (legacy routes — keep for existing references) ───────────────
    path("users/", views.manage_users, name="manage_users"),
    path("users/add/", views.add_user, name="add_user"),
    path("users/<int:user_id>/reset-password/", views.reset_user_password, name="reset_user_password"),
    path("users/<int:user_id>/toggle-active/", views.toggle_user_active, name="toggle_user_active"),
    path("users/<int:user_id>/change-role/", views.change_user_role, name="change_user_role"),
    path("users/<int:user_id>/delete/", views.delete_user, name="delete_user"),

    # ─── Users (new routes — used by manage_users.html inline edit) ─────────
    path("users/create/", views.user_create_view, name="user_create"),
    path("users/<int:user_id>/edit/", views.user_edit_view, name="user_edit"),
    path("users/<int:user_id>/delete-new/", views.user_delete_view, name="user_delete"),

    # ─── Teams ──────────────────────────────────────────────────────────────
    path("teams/", views.manage_teams, name="manage_teams"),
    path("teams/create/", views.team_create_view, name="team_create"),
    path("teams/<int:team_id>/edit/", views.team_edit_view, name="team_edit"),
    path("teams/<int:team_id>/delete/", views.team_delete_view, name="team_delete"),

    # ─── Departments ─────────────────────────────────────────────────────────
    path("departments/", views.manage_departments, name="manage_departments"),
    path("departments/create/", views.department_create_view, name="department_create"),
    path("departments/<int:dept_id>/edit/", views.department_edit_view, name="department_edit"),
    path("departments/<int:dept_id>/delete/", views.department_delete_view, name="department_delete"),

    # ─── Projects ────────────────────────────────────────────────────────────
    path("projects/", views.manage_projects, name="manage_projects"),
    path("projects/create/", views.project_create_view, name="project_create"),
    path("projects/<int:project_id>/edit/", views.project_edit_view, name="project_edit"),
    path("projects/<int:project_id>/delete/", views.project_delete_view, name="project_delete"),

    # ─── Dependencies ────────────────────────────────────────────────────────
    path("dependencies/", views.manage_dependencies, name="manage_dependencies"),
    path("dependencies/create/", views.dependency_create_view, name="dependency_create"),
    path("dependencies/<int:dep_id>/edit/", views.dependency_edit_view, name="dependency_edit"),
    path("dependencies/<int:dep_id>/delete/", views.dependency_delete_view, name="dependency_delete"),
]