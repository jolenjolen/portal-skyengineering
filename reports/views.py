"""
Authors: Muhammed Hasan (w1689191)
Decription: Create reports for display
"""

import csv
from django.shortcuts import render
from django.http import HttpResponse
from core.models import TblTeam, TblDepartment, TblProject, TblDependencies
from accounts.views import is_logged_in
from django.shortcuts import redirect
from accounts.views import is_admin


def reports_dashboard(request):
    if not is_logged_in(request):
        return redirect("login")
    """
    Main Reports page
    Shows summary values and identifies teams missing a team leader
    """

    # Summary figures
    total_teams = TblTeam.objects.count()
    total_departments = TblDepartment.objects.count()
    total_projects = TblProject.objects.count()
    teams_no_leader = TblTeam.objects.filter(team_leader__isnull=True)

    # teams per department report
    department_report = []

    for department in TblDepartment.objects.all():
        # counts the number of teams in each department
        team_count = TblTeam.objects.filter(department=department).count()

        # adds to department report
        department_report.append(
            {
                "department": department.name,
                "team_count": team_count,
            }
        )

    # Projects per team report
    project_report = []

    for team in TblTeam.objects.all():
        project_names_holder = TblProject.objects.filter(team=team)
        project_count = project_names_holder.count()
        project_names = [project.name for project in project_names_holder]

        project_report.append(
            {
                "team_name": team.name,
                "projects": project_names,
                "project_count": project_count,
            }
        )

    # Dependency report
    dependency_report = []

    for dependency in TblDependencies.objects.select_related("team").all():
        dependency_report.append(
            {
                "team_name": dependency.team.name if dependency.team else "No team",
                "depends_on": dependency.dependency_team_name or "Not specified",
                "dependency_type": dependency.type or "Not specified",
                "direction": "Downstream" if dependency.downstream else "Upstream",
            }
        )

    # Store values
    context = {
        "total_teams": total_teams,
        "total_departments": total_departments,
        "total_projects": total_projects,
        "teams_no_leader": teams_no_leader,
        "department_report": department_report,
        "project_report": project_report,
        "dependency_report": dependency_report,
        "is_admin_user": is_admin(request),
    }

    return render(request, "reports/dashboard.html", context)


# create reports csv function
def export_team_report_csv(request):
    if not is_logged_in(request):
        return redirect("login")
    # downloads team report with team summary
    csv_response = HttpResponse(content_type="text/csv")
    csv_response["Content-Disposition"] = 'attachment; filename="Sky_Teams_Summary.csv"'

    csv_writer = csv.writer(csv_response)

    csv_writer.writerow(
        [
            "Team",
            "Department",
            "Leader",
            "Skills",
            "Agile Practices",
            "Slack",
            "Wiki",
            "Active Projects",
        ]
    )

    team_records = TblTeam.objects.select_related("department", "team_leader").all()

    for team_record in team_records:
        csv_writer.writerow(
            [
                team_record.name,
                (
                    team_record.department.name
                    if team_record.department
                    else "No department"
                ),
                (
                    f"{team_record.team_leader.fname} {team_record.team_leader.sname}"
                    if team_record.team_leader
                    else "No leader"
                ),
                team_record.skills_and_tech or "",
                team_record.agile_practices or "",
                team_record.slack or "",
                team_record.wiki or "",
                (
                    team_record.active_projects
                    if team_record.active_projects is not None
                    else ""
                ),
            ]
        )

    # department reports
    csv_writer.writerow([])
    csv_writer.writerow(["Teams Per Department"])
    csv_writer.writerow(["Department", "Number of Teams"])

    for department in TblDepartment.objects.all():
        team_count = TblTeam.objects.filter(department=department).count()

        csv_writer.writerow([department.name, team_count])

    # project reports
    csv_writer.writerow([])
    csv_writer.writerow(["Projects Per Team"])
    csv_writer.writerow(["Team", "Projects", "Number of projects"])

    for team in TblTeam.objects.all():
        project_names_holder = TblProject.objects.filter(team=team)
        project_count = project_names_holder.count()
        project_names = [project.name for project in project_names_holder]

        csv_writer.writerow(
            [
                team.name,
                ", ".join(project_names) if project_names else "No projects",
                project_count,
            ]
        )

    # Dependency report
    csv_writer.writerow([])
    csv_writer.writerow(["Dependency Report"])
    csv_writer.writerow(["Team", "Depends On", "Dependency Type", "Direction"])

    for dependency in TblDependencies.objects.select_related("team").all():
        csv_writer.writerow(
            [
                dependency.team.name if dependency.team else "No team",
                dependency.dependency_team_name or "Not specified",
                (
                    dependency.type or "Not specified" "Downstream"
                    if dependency.downstream
                    else "Upstream"
                ),
            ]
        )

    return csv_response


def visualisations_view(request):
    if not is_logged_in(request):
        return redirect("login")
    return render(request, "reports/visualisations.html")
