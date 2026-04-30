# Author: jolen Mascarenhas (w2078969)
from django.urls import path
from .views import login_view, signup_view, help_view, contact_view, reset_password_view, privacy_policy, tos, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('help/', help_view, name='help'),
    path('contact/', contact_view, name='contact'),
    path('password-reset/', reset_password_view, name='password_reset'), 
    path('password-reset/', reset_password_view, name='password_reset'), 
    path('pp/', privacy_policy, name='pp'), 
    path('tos/', tos, name='tos'),
    path('logout/', logout_view, name='logout'),
]