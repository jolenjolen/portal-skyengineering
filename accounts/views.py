from django.shortcuts import render, redirect
from django.utils import timezone
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
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = TblUser.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            return redirect('dashboard_home')  # Redirect to dashboard_home after login
        except TblUser.DoesNotExist:
            error = "Invalid credentials"
    return render(request, 'accounts/login.html', {'error': error})

# Signup page
def signup_view(request):
    error = None
    if request.method == 'POST':
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if TblUser.objects.filter(email=email).exists():
            error = "Email already exists"
        else:
            TblUser.objects.create(
                fname=fname,
                email=email,
                password=password,
                created=timezone.now(),
                active=True
            )
            return redirect('login')
    return render(request, 'accounts/signup.html', {'error': error})

# Help page
def help_view(request):
    return render(request, 'accounts/help.html')

# Contact page
def contact_view(request):
    return render(request, 'accounts/contact.html')

# Home page (landing after login)
def template_view(request):
    if not is_logged_in(request):
        return redirect('login')
    return render(request, 'accounts/template.html')