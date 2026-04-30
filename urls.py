#Author: Jolen Mascarenhas (w2078969)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),  # Root points to dashboard
    path('accounts/', include('accounts.urls')),  # Login/signup under /accounts/
]