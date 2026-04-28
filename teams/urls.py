"""
Author: [Your Name]
Description: URL routing for the Teams app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.teams_list, name='teams_list'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
]
