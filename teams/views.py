"""
Author: [Your Name]
Description: Teams page views — list all teams with search/filter, team detail with
             skills, dependencies (upstream/downstream), email and schedule meeting actions.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from core.models import TblTeam, TblDepartment, TblUser, TblDependencies
from core.utils import login_required
from accounts.views import is_admin, current_user


@login_required
def teams_list(request):
    """
    Display all engineering teams in a searchable table.
    Supports live filtering by team name, department, or manager name via GET param 'q'.
    """
    query = request.GET.get('q', '').strip()

    teams = TblTeam.objects.select_related('department', 'team_leader').all().order_by('name')

    if query:
        teams = teams.filter(name__icontains=query) | \
                TblTeam.objects.select_related('department', 'team_leader').filter(
                    department__name__icontains=query
                ) | \
                TblTeam.objects.select_related('department', 'team_leader').filter(
                    team_leader__fname__icontains=query
                ) | \
                TblTeam.objects.select_related('department', 'team_leader').filter(
                    team_leader__sname__icontains=query
                )
        teams = teams.distinct().order_by('name')

    context = {
        'teams': teams,
        'query': query,
        'is_admin_user': is_admin(request),
        'current_user': current_user(request),
    }
    return render(request, 'teams/teams_list.html', context)


@login_required
def team_detail(request, team_id):
    """
    Show full details of a single team including members, skills, dependencies,
    contact channels and code repositories.
    """
    team = get_object_or_404(TblTeam, id=team_id)

    # Team members (all users who belong to this team)
    members = TblUser.objects.filter(team=team, active=True)

    # Skills — stored as comma-separated string in skills_and_tech
    skills = []
    if team.skills_and_tech:
        skills = [s.strip() for s in team.skills_and_tech.split(',') if s.strip()]

    # Dependencies
    upstream_deps = TblDependencies.objects.filter(team=team, upstream=True)
    downstream_deps = TblDependencies.objects.filter(team=team, downstream=True)

    context = {
        'team': team,
        'members': members,
        'skills': skills,
        'upstream_deps': upstream_deps,
        'downstream_deps': downstream_deps,
        'is_admin_user': is_admin(request),
        'current_user': current_user(request),
    }
    return render(request, 'teams/team_detail.html', context)
