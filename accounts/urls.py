from django.urls import path
from .views import (
    login_view, signup_view, template_view,
    help_view, contact_view, index_view
)

urlpatterns = [
    path('', index_view, name='home'),            # Main root page
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('help/', help_view, name='help'),
    path('contact/', contact_view, name='contact'),
    path('template/', template_view, name='template'),
]