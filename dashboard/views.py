from django.shortcuts import render, redirect

# Main index page
def index_view(request):
    # Optional: check if user is logged in via session
    if not request.session.get('user_id'):
        from django.shortcuts import redirect
        return redirect('login')  # redirect to accounts login if not logged in
    return render(request, 'dashboard/index.html')