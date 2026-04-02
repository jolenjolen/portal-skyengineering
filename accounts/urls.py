from django.urls import path
from .views import login_view, signup_view, help_view, contact_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('help/', help_view, name='help'),
    path('contact/', contact_view, name='contact'),
]