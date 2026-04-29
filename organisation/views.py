from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from core.models import TblDepartment, TblTeam, TblDependencies, TblUser


def login_required_custom(view_func):
    """Check session-based login used by this project."""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@login_required_custom
def organisation_overview(request):
    departments = TblDepartment.objects.all()
    dept_data = []
    for dept in departments:
        teams = TblTeam.objects.filter(department=dept)
        dept_data.append({
            'dept': dept,
            'teams': teams,
            'team_count': teams.count(),
            'head': dept.department_head,
        })
    context = {
        'dept_data': dept_data,
        'total_teams': TblTeam.objects.count(),
        'total_depts': departments.count(),
        'total_members': TblUser.objects.filter(active=True).count(),
    }
    return render(request, 'organisation/overview.html', context)


@login_required_custom
def department_list(request):
    query = request.GET.get('q', '')
    departments = TblDepartment.objects.all()
    if query:
        departments = departments.filter(name__icontains=query)
    dept_data = []
    for dept in departments:
        teams = TblTeam.objects.filter(department=dept)
        dept_data.append({
            'dept': dept,
            'teams': teams,
            'team_count': teams.count(),
        })
    return render(request, 'organisation/department_list.html', {'dept_data': dept_data, 'query': query})


@login_required_custom
def department_detail(request, dept_id):
    dept = get_object_or_404(TblDepartment, id=dept_id)
    teams = TblTeam.objects.filter(department=dept)
    teams_with_members = []
    for team in teams:
        members = TblUser.objects.filter(team=team)
        teams_with_members.append({
            'team': team,
            'members': members,
            'member_count': members.count(),
            'upstream_deps': TblDependencies.objects.filter(team=team, upstream=True),
            'downstream_deps': TblDependencies.objects.filter(team=team, downstream=True),
        })
    return render(request, 'organisation/department_detail.html', {
        'dept': dept,
        'teams_with_members': teams_with_members,
        'team_count': teams.count(),
    })


@login_required_custom
def org_chart(request):
    departments = TblDepartment.objects.all()
    chart_data = []
    for dept in departments:
        teams = TblTeam.objects.filter(department=dept)
        team_list = []
        for team in teams:
            members = TblUser.objects.filter(team=team)
            team_list.append({'team': team, 'members': members, 'member_count': members.count()})
        chart_data.append({'dept': dept, 'teams': team_list, 'team_count': teams.count()})
    return render(request, 'organisation/org_chart.html', {'chart_data': chart_data})


@login_required_custom
def dependencies_view(request):
    query = request.GET.get('q', '')
    dep_type = request.GET.get('type', 'all')
    teams = TblTeam.objects.all()
    if query:
        teams = teams.filter(name__icontains=query)
    teams_deps = []
    for team in teams:
        upstream = TblDependencies.objects.filter(team=team, upstream=True)
        downstream = TblDependencies.objects.filter(team=team, downstream=True)
        if dep_type == 'upstream' and not upstream.exists():
            continue
        if dep_type == 'downstream' and not downstream.exists():
            continue
        teams_deps.append({'team': team, 'upstream': upstream, 'downstream': downstream})
    return render(request, 'organisation/dependencies.html', {
        'teams_deps': teams_deps, 'query': query, 'dep_type': dep_type,
    })


@login_required_custom
def team_type_view(request):
    dept_query = request.GET.get('dept', '')
    all_depts = TblDepartment.objects.all()
    departments = all_depts
    if dept_query:
        departments = departments.filter(id=dept_query)
    grouped = []
    for dept in departments:
        teams = TblTeam.objects.filter(department=dept)
        grouped.append({'dept': dept, 'teams': teams, 'count': teams.count()})
    return render(request, 'organisation/team_type.html', {
        'grouped': grouped, 'all_depts': all_depts, 'selected_dept': dept_query,
    })