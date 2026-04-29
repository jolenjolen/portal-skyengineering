from django.shortcuts import render, redirect, get_object_or_404
from core.models import TblDepartment, TblTeam, TblProject
from accounts.views import is_logged_in


def department_list(request):
    # security measures to ensure user is logged in
    if not is_logged_in(request):
        return redirect("login")

    department_report = []
    # loop to get department information
    for department in TblDepartment.objects.all():
        # counts number of teams in that specific department
        total_teams = TblTeam.objects.filter(department=department).count()

        department_report.append(
            {
                "id": department.id,
                "name": department.name,
                "head": department.department_head,
                "team_count": total_teams,
            }
        )

        context = {
            "department_report": department_report,
        }

    return render(request, "departments/department_list.html", context)


def department_details(request, deparment_id):
    # security measures to ensure user is logged in
    if not is_logged_in(request):
        return redirect("login")

    department = get_object_or_404(TblDepartment, id=deparment_id)

    team_report = []

    teams = TblTeam.objects.filter(department=department)

    for team in teams:
        projects = TblProject.objects.filter(team=team)
        project_names = [project.name for project in projects]

        team_report.apppend(
            {
                "team_name": team.name,
                "projects": project_names,
                "project_count": projects.count(),
            }
        )

        context = {
            "department": department,
            "team_report": team_report,
        }

    return render(request, "departments/department_detail.html", context)
