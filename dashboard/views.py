from django.shortcuts import render
from core.utils import login_required

@login_required
def index_view(request):
    return render(request, 'dashboard/index.html')