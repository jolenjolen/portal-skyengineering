#author: Jolen Mascarenhas (w2078969), Muhammed Hasan (w1689191)
from django.shortcuts import render
from core.utils import login_required
from accounts.views import is_admin

@login_required
def index_view(request):
    context={
        "is_admin_user": is_admin(request),
    }
    return render(request, 'dashboard/index.html', context)