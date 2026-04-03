from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from core.models import TblUser

# Helper to check if user is logged in
def is_logged_in(request):
    return request.session.get('user_id') is not None

# Main index page
def index_view(request):
    if not is_logged_in(request):
        return redirect('login')
    return render(request, 'accounts/index.html')

# Login page
def login_view(request):
    # If already logged in, skip the login page
    if is_logged_in(request):
        return redirect('home')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = TblUser.objects.get(uname=username, active=True)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                return redirect('home')
            else:
                error = "Invalid credentials"
        except TblUser.DoesNotExist:
            error = "Invalid credentials"
    return render(request, 'accounts/login.html', {'error': error})

# Logout
def logout_view(request):
    if request.method == 'POST':
        request.session.flush()
        return redirect('login')
    return redirect('home')  # if someone hits /logout directly via GET, just send them home

def reset_password_view(request):
    return render(request, 'accounts/password_reset.html')

# Signup page — just render for now, admin creates users manually
def signup_view(request):
    return render(request, 'accounts/signup.html')

# Help page
def help_view(request):
    return render(request, 'accounts/help.html')

# Contact page
def contact_view(request):
    return render(request, 'accounts/contact.html')


def privacy_policy(request):
    return render(request, 'accounts/pp.html')

def tos(request):
    return render(request, 'accounts/tos.html')