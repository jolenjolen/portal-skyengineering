from django.shortcuts import render
from django.db.models import Q
from core.utils import login_required
from core.models import TblTeam, TblDependencies
from accounts.views import is_admin

@login_required
def index_view(request):
    context={
        "is_admin_user": is_admin(request),
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def teams_view(request):
    """
    Teams page - shows all teams with search, skills, dependencies,
    and quick-actions to email the team leader or schedule a meeting.
    """
    query = (request.GET.get('q') or '').strip()

    teams_qs = TblTeam.objects.select_related('department', 'team_leader').all().order_by('name')

    if query:
        teams_qs = teams_qs.filter(
            Q(name__icontains=query)
            | Q(department__name__icontains=query)
            | Q(team_leader__fname__icontains=query)
            | Q(team_leader__sname__icontains=query)
            | Q(skills_and_tech__icontains=query)
        )

    # Pull dependencies in one query and group them by team id
    deps_by_team = {}
    for dep in TblDependencies.objects.all():
        team_id = dep.team_id
        if team_id is None:
            continue
        deps_by_team.setdefault(team_id, []).append({
            'name': dep.dependency_team_name or 'Unspecified',
            'type': dep.type or 'Unspecified',
            'direction': 'Downstream' if dep.downstream else ('Upstream' if dep.upstream else 'Unknown'),
        })

    teams = []
    for team in teams_qs:
        leader = team.team_leader
        if leader:
            leader_name = f"{leader.fname} {leader.sname or ''}".strip()
            leader_email = leader.email
        else:
            leader_name = 'No leader assigned'
            leader_email = ''

        skills = [s.strip() for s in (team.skills_and_tech or '').split(',') if s.strip()]

        teams.append({
            'id': team.id,
            'name': team.name,
            'department': team.department.name if team.department else 'No department',
            'leader_name': leader_name,
            'leader_email': leader_email,
            'description': team.description or '',
            'skills': skills,
            'slack': team.slack or '',
            'wiki': team.wiki or '',
            'dependencies': deps_by_team.get(team.id, []),
        })

    context = {
        'is_admin_user': is_admin(request),
        'teams': teams,
        'query': query,
        'total_count': len(teams),
    }
    return render(request, 'dashboard/teams.html', context)