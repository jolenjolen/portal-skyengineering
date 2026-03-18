from django.utils import timezone
from django.shortcuts import render, redirect
from core.models import TblUser

def login_view(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = TblUser.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            return redirect('/')
        except TblUser.DoesNotExist:
            error = "Invalid credentials"

    return render(request, 'accounts/login.html', {'error': error})

def signup_view(request):
    error = None

    if request.method == 'POST':
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

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
            return redirect('/login/')

    return render(request, 'accounts/signup.html', {'error': error})
