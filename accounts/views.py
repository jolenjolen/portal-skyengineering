"""
Authors:
Muhammed Hasan (w1689191): Admin access, defined users and admin.
Dervish Denaj (w1984059): added profile and changing password. 
"""

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from core.models import TblUser, TblTeam

# Helper to check if user is logged in
def is_logged_in(request):
    return request.session.get('user_id') is not None

#Finds the user who is currently logged in
def current_user(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return None
    
    try:
        return TblUser.objects.get(id=user_id)
    except TblUser.DoesNotExist:
        return None

# Helper to check if user is an admin
def is_admin(request):
    user = current_user(request)
    return user is not None and user.role == "Admin"

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

# Profile page 
def profile_view(request):
    if not is_logged_in(request):
        return redirect('login')
    user = current_user(request)
    error = None
    success = None
    teams = TblTeam.objects.all()

    if request.method == 'POST':
        # Read submitted form fields
        fname = request.POST.get('fname', '').strip()
        sname = request.POST.get('sname', '').strip()
        uname = request.POST.get('uname', '').strip()
        email = request.POST.get('email', '').strip()
        role = request.POST.get('role', '').strip()
        team_id = request.POST.get('team')
        department_name = request.POST.get('department', '').strip()

        if not fname or not uname or not email:
            error = 'First name, username and email are required.'
        else:
            # updates the fields in the database
            user.fname = fname
            user.sname = sname
            user.uname = uname
            user.email = email
            user.role = role
            user.team = TblTeam.objects.filter(pk=team_id).first() if team_id else None
            user.save(update_fields=['fname', 'sname', 'uname', 'email', 'role', 'team'])
            # Update the department name if provided
            if user.team and user.team.department and department_name:
                user.team.department.name = department_name
                user.team.department.save(update_fields=['name'])
            success = 'Profile updated successfully.'

    return render(request, 'accounts/profile.html', {
        'user': user,
        'error': error,
        'success': success,
        'teams': teams,
    })

# page to change password
def change_password_view(request):
    if not is_logged_in(request):
        return redirect('login')
    user = current_user(request)
    error = None
    success = None

    if request.method == 'POST':
        new = request.POST.get('new_password', '')
        user.password = make_password(new)
        user.save(update_fields=['password'])
        success = 'Password changed successfully.'

    return render(request, 'accounts/profile.html', {
        'user': user,
        'error': error,
        'success': success,
        'password_tab': True,
    })