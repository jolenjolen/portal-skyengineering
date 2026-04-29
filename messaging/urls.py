"""
Author: Marta Pikturnaite (w2073431)
"""
from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('drafts/', views.drafts, name='drafts'),
    path('new/', views.new_message, name='new_message'),
    path('<int:pk>/', views.view_message, name='view_message'),
    path('draft/<int:pk>/send/', views.send_draft, name='send_draft'),
    path('draft/<int:pk>/edit/', views.edit_draft, name='edit_draft'),
]