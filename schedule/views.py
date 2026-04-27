'''
Authors: Dervish Denaj(w1984059)
Description: Views for managing and displaying meetings by different schedule
'''

from django.shortcuts import render, redirect
from django.utils import timezone
from core.utils import login_required
from accounts.views import is_admin
from .models import Meeting


@login_required
def dashboard_view(request):
    # all meetings sorted chronologically
    events = Meeting.objects.order_by('date', 'time')
    return render(request, 'schedule/dashboard.html', {
        'is_admin_user': is_admin(request),
        'events': events,
    })


@login_required
def create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        meeting_link = request.POST.get('meeting_link', '')
        Meeting.objects.create(title=title, date=date, time=time, meeting_link=meeting_link)
        return redirect('schedule')
    # GET request just renders the empty form
    return render(request, 'schedule/create.html', {'is_admin_user': is_admin(request)})


@login_required
def monthly_view(request):
    today = timezone.now().date()
    # filter to current month only
    events = Meeting.objects.filter(
        date__year=today.year, date__month=today.month
    ).order_by('date', 'time')
    return render(request, 'schedule/monthly.html', {
        'is_admin_user': is_admin(request),
        'events': events,
        'month': today.strftime('%B %Y'),
    })


@login_required
def weekly_view(request):
    today = timezone.now().date()
    # weekday() returns 0 for Monday, so this gives the Monday of the current week
    week_start = today - timezone.timedelta(days=today.weekday())
    week_end = week_start + timezone.timedelta(days=6)
    events = Meeting.objects.filter(
        date__gte=week_start, date__lte=week_end
    ).order_by('date', 'time')
    return render(request, 'schedule/weekly.html', {
        'is_admin_user': is_admin(request),
        'events': events,
        'week_start': week_start,
        'week_end': week_end,
    })
