'''
Authors: Dervish Denaj(w1984059)
Description: Views for managing and displaying meetings by different schedule
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from core.utils import login_required
from core.models import TblTeam
from accounts.views import is_admin, current_user
from .models import Meeting


def get_led_team(user):
    """Returns the team this user leads, or None."""
    return TblTeam.objects.filter(team_leader=user).first()


@login_required
def dashboard_view(request):
    user = current_user(request)
    admin = is_admin(request)
    led_team = get_led_team(user)
    today = timezone.now().date()
    show_past = request.GET.get('view') == 'past'

    if admin:
        qs = Meeting.objects.all()
    else:
        qs = Meeting.objects.filter(team=user.team)

    if show_past:
        events = qs.filter(date__lt=today).order_by('-date', '-time')
    else:
        events = qs.filter(date__gte=today).order_by('date', 'time')

    return render(request, 'schedule/dashboard.html', {
        'is_admin_user': admin,
        'events': events,
        'show_past': show_past,
        'led_team': led_team,
    })


@login_required
def create_view(request):
    user = current_user(request)
    admin = is_admin(request)
    led_team = get_led_team(user)

    if not admin and not led_team:
        return redirect('schedule')

    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        meeting_link = request.POST.get('meeting_link', '')
        message = request.POST.get('message', '')

        if admin:
            team_id = request.POST.get('team')
            team = TblTeam.objects.filter(pk=team_id).first() if team_id else None
        else:
            team = led_team

        Meeting.objects.create(
            title=title, date=date, time=time,
            meeting_link=meeting_link, message=message, team=team
        )
        return redirect('schedule')

    teams = TblTeam.objects.all() if admin else None
    return render(request, 'schedule/create.html', {
        'is_admin_user': admin,
        'led_team': led_team,
        'teams': teams,
    })


@login_required
def edit_view(request, pk):
    user = current_user(request)
    admin = is_admin(request)
    led_team = get_led_team(user)
    meeting = get_object_or_404(Meeting, pk=pk)

    if not admin and meeting.team != led_team:
        return redirect('schedule')

    if request.method == 'POST':
        meeting.title = request.POST.get('title')
        meeting.date = request.POST.get('date')
        meeting.time = request.POST.get('time')
        meeting.meeting_link = request.POST.get('meeting_link', '')
        meeting.message = request.POST.get('message', '')
        if admin:
            team_id = request.POST.get('team')
            meeting.team = TblTeam.objects.filter(pk=team_id).first() if team_id else None
        meeting.save()
        return redirect('schedule')

    teams = TblTeam.objects.all() if admin else None
    return render(request, 'schedule/edit.html', {
        'is_admin_user': admin,
        'meeting': meeting,
        'teams': teams,
        'led_team': led_team,
    })


@login_required
def delete_view(request, pk):
    user = current_user(request)
    admin = is_admin(request)
    led_team = get_led_team(user)
    meeting = get_object_or_404(Meeting, pk=pk)

    if not admin and meeting.team != led_team:
        return redirect('schedule')

    if request.method == 'POST':
        meeting.delete()
    return redirect('schedule')


@login_required
def monthly_view(request):
    user = current_user(request)
    admin = is_admin(request)
    led_team = get_led_team(user)
    today = timezone.now().date()

    if admin:
        qs = Meeting.objects.all()
    else:
        qs = Meeting.objects.filter(team=user.team)

    events = qs.filter(
        date__year=today.year, date__month=today.month
    ).order_by('date', 'time')

    return render(request, 'schedule/monthly.html', {
        'is_admin_user': admin,
        'events': events,
        'month': today.strftime('%B %Y'),
        'led_team': led_team,
    })


@login_required
def weekly_view(request):
    user = current_user(request)
    admin = is_admin(request)
    led_team = get_led_team(user)
    today = timezone.now().date()
    week_start = today - timezone.timedelta(days=today.weekday())
    week_end = week_start + timezone.timedelta(days=6)

    if admin:
        qs = Meeting.objects.all()
    else:
        qs = Meeting.objects.filter(team=user.team)

    events = qs.filter(
        date__gte=week_start, date__lte=week_end
    ).order_by('date', 'time')

    return render(request, 'schedule/weekly.html', {
        'is_admin_user': admin,
        'events': events,
        'week_start': week_start,
        'week_end': week_end,
        'led_team': led_team,
    })
