from django.urls import path
from .views import dashboard_view, create_view, monthly_view, weekly_view

urlpatterns = [
    path('', dashboard_view, name='schedule'),
    path('create/', create_view, name='schedule_create'),
    path('monthly/', monthly_view, name='schedule_monthly'),
    path('weekly/', weekly_view, name='schedule_weekly'),
]