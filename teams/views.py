"""
Author: <YOUR NAME / STUDENT ID HERE>
Description:
    Views for the Teams app (CWK1/CWK2 individual task — Student 1).

    This module implements the three pages backing the Teams menu item:
      * team_list_view             — main "Engineering Teams" table page
                                     with working search, inline skills,
                                     dependency counts and quick-action
                                     buttons (email / schedule meeting).
      * team_detail_view           — "learn more" page that shows the
                                     team's full skills, upstream and
                                     downstream dependencies, members,
                                     and contact channels.
      * team_schedule_meeting_view — small form that lets any logged-in
                                     user request a meeting with a team.
                                     The submission writes to the existing
                                     schedule.Meeting table so the new
                                     meeting also shows up in the Schedule
                                     pages built by another team member.

Notes:
  - We re-use the existing models in core.models (TblTeam, TblUser,
    TblDependencies). The teams/models.py file is intentionally empty
    — see its docstring.
  - Auth uses the project's session-based helper (core.utils.login_required
    + accounts.views.is_admin / current_user) so the experience is the
    same as every other page in the portal.
"""

from django.db.models import Q, Count, Case, When, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as flash_messages

from core.utils import login_required
from core.models import TblTeam, TblUser, TblDependencies
from accounts.views import is_admin, current_user
from schedule.models import Meeting


def _split_skills(raw):
    """
    The skills_and_tech column stores a single comma-separated string
    (e.g. "Python, Django, AWS"). This helper splits it into a clean
    list, dropping empty entries that come from trailing commas etc.
    """
    if not raw:
        return []
    return [s.strip() for s in raw.split(',') if s.strip()]


@login_required
def team_list_view(request):
    """
    Show all teams in a table that matches the storyboard layout.

    Search:
        ?q=<text>  — filters teams where the text appears (case-insensitive)
        in any of: team name, department name, manager first/last name,
        skills_and_tech.

    For each team we also attach:
        - team.skill_list:        list of skills (split on commas)
        - team.upstream_count:    how many upstream dependencies it has
        - team.downstream_count:  how many downstream dependencies it has
    so the template can render the inline badges without needing to do
    its own queries.
    """
    query = request.GET.get('q', '').strip()

    teams_qs = TblTeam.objects.select_related('department', 'team_leader').all()

    if query:
        teams_qs = teams_qs.filter(
            Q(name__icontains=query)
            | Q(department__name__icontains=query)
            | Q(team_leader__fname__icontains=query)
            | Q(team_leader__sname__icontains=query)
            | Q(skills_and_tech__icontains=query)
        )

    # Annotate dependency counts with a single query each, instead of
    # hitting the DB once per row in the template (avoids the N+1 problem).
    teams_qs = teams_qs.annotate(
        upstream_count=Count(
            Case(When(tbldependencies__upstream=True, then=1),
                 output_field=IntegerField())
        ),
        downstream_count=Count(
            Case(When(tbldependencies__downstream=True, then=1),
                 output_field=IntegerField())
        ),
    ).order_by('name')

    teams = list(teams_qs)
    for team in teams:
        team.skill_list = _split_skills(team.skills_and_tech)

    context = {
        'teams': teams,
        'query': query,
        'result_count': len(teams),
        'is_admin_user': is_admin(request),
    }
    return render(request, 'teams/team_list.html', context)


@login_required
def team_detail_view(request, team_id):
    """
    Detailed "learn more" view for a single team. Shows the team's full
    description, skills (as badges), upstream and downstream dependencies,
    contact channels (email, Slack, wiki) and members.
    """
    team = get_object_or_404(
        TblTeam.objects.select_related('department', 'team_leader'),
        pk=team_id,
    )

    # All members of this team — i.e. tbl_user rows whose FK points here.
    members = TblUser.objects.filter(team=team).order_by('fname', 'sname')

    # The schema records each direction as its own row using the boolean
    # flags, so we filter on them to split into the two lists the
    # template expects.
    upstream_deps = TblDependencies.objects.filter(
        team=team, upstream=True,
    ).order_by('id')
    downstream_deps = TblDependencies.objects.filter(
        team=team, downstream=True,
    ).order_by('id')

    skills = _split_skills(team.skills_and_tech)

    context = {
        'team': team,
        'members': members,
        'upstream_deps': upstream_deps,
        'downstream_deps': downstream_deps,
        'skills': skills,
        'is_admin_user': is_admin(request),
    }
    return render(request, 'teams/team_detail.html', context)


@login_required
def team_schedule_meeting_view(request, team_id):
    """
    Lets any logged-in user request a meeting with the given team.

    On POST we validate the required fields (title, date, time) and
    create a new Meeting row attached to the team. We deliberately
    re-use the schedule app's model so the new meeting also appears
    in the existing Schedule pages (dashboard / weekly / monthly).
    """
    team = get_object_or_404(TblTeam, pk=team_id)
    user = current_user(request)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        date = request.POST.get('date')
        time = request.POST.get('time')
        meeting_link = request.POST.get('meeting_link', '').strip()
        message = request.POST.get('message', '').strip()

        if not title or not date or not time:
            flash_messages.error(request, 'Title, date and time are required.')
        else:
            who = f"{user.fname} {user.sname}" if user else 'A user'
            note = message or f"Meeting requested by {who} via the Teams page."
            Meeting.objects.create(
                title=title,
                date=date,
                time=time,
                meeting_link=meeting_link,
                message=note,
                team=team,
            )
            flash_messages.success(
                request,
                f"Meeting '{title}' scheduled with {team.name}.",
            )
            return redirect('team_detail', team_id=team.id)

    context = {
        'team': team,
        'is_admin_user': is_admin(request),
    }
    return render(request, 'teams/schedule_meeting.html', context)
