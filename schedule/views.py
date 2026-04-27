from django.shortcuts import render
from core.utils import login_required
from accounts.views import is_admin


@login_required
def index_view(request):
    return render(request, 'schedule/index.html', {'is_admin_user': is_admin(request)})
