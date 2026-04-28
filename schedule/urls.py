from django.urls import path
from .views import dashboard_view, create_view, edit_view, delete_view, monthly_view, weekly_view

urlpatterns = [
    path('', dashboard_view, name='schedule'),
    path('create/', create_view, name='schedule_create'),
    path('edit/<int:pk>/', edit_view, name='schedule_edit'),
    path('delete/<int:pk>/', delete_view, name='schedule_delete'),
    path('monthly/', monthly_view, name='schedule_monthly'),
    path('weekly/', weekly_view, name='schedule_weekly'),
]