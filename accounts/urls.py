from django.urls import path
from .views import login_view, signup_view, template_view

urlpatterns = [
    path('', template_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
]
