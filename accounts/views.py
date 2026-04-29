"""
Authors:
Muhammed Hasan (w1689191): Admin access, defined users and admin.
Dervish Denaj (w1984059): added profile and changing password. 
Jolen Mascarenhas (w1689192): Login/logout, password hashing, session management.
"""

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from core.models import TblUser
from messaging.models import Message

def contact_view(request):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        message_body = request.POST.get('message')

        # Extra fields depending on reason
        email = request.POST.get('email', '')
        department = request.POST.get('department', '')
        page_affected = request.POST.get('page_affected', '')
        browser = request.POST.get('browser', '')

        reason_labels = {
            'forgot_password': 'Forgot Password',
            'enquiry': 'General Enquiry',
            'system_issue': 'System Issue',
            'account_locked': 'Account Locked',
            'other': 'Other',
        }

        subject = f"[Contact Admin] {reason_labels.get(reason, 'Request')}"

        extra = ''
        if email:
            extra += f"Email: {email}\n"
        if department:
            extra += f"Department: {department}\n"
        if page_affected:
            extra += f"Page Affected: {page_affected}\n"
        if browser:
            extra += f"Browser/Device: {browser}\n"

        body = (
            f"Reason: {reason_labels.get(reason, reason)}\n"
            f"Full Name: {full_name}\n"
            f"Username: {username}\n"
            f"{extra}\n"
            f"Message:\n{message_body}"
        )

        # Get guest user as sender (sender cannot be null)
        try:
            guest_user = TblUser.objects.get(uname='guest')
        except TblUser.DoesNotExist:
            return render(request, 'accounts/contact.html', {
                'error': 'System error: guest account not configured. Please contact your administrator directly.'
            })

        # Get all admins
        admins = TblUser.objects.filter(role='Admin')

        if not admins.exists():
            return render(request, 'accounts/contact.html', {
                'error': 'No admins found. Please try again later.'
            })

        try:
            for admin in admins:
                Message.objects.create(
                    sender=guest_user,
                    recipient=admin,
                    subject=subject,
                    body=body,
                    status='sent'
                )
            admin_count = admins.count()
            return render(request, 'accounts/contact.html', {
                'success': f'Your message has been sent. An admin will get back to you shortly.'
            })
        except Exception as e:
            return render(request, 'accounts/contact.html', {
                'error': f'Something went wrong: {str(e)}'
            })

    return render(request, 'accounts/contact.html')

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

    if request.method == 'POST':
        # Read submitted form fields
        fname = request.POST.get('fname', '').strip()
        sname = request.POST.get('sname', '').strip()
        uname = request.POST.get('uname', '').strip()

        if not fname or not uname:
            error = 'First name and username are required.'
        else:
            # updates the fields in the database
            user.fname = fname
            user.sname = sname
            user.uname = uname
            user.save(update_fields=['fname', 'sname', 'uname'])
            success = 'Profile updated successfully.'

    return render(request, 'accounts/profile.html', {
        'user': user,
        'error': error,
        'success': success,
        'is_admin_user': is_admin(request),
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
        'is_admin_user': is_admin(request),
    })