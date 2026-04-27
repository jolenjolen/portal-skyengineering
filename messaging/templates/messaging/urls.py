from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('drafts/', views.drafts, name='drafts'),
    path('new/', views.new_message, name='new_message'),
    path('<int:pk>/', views.view_message, name='view_message'),
]