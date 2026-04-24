import csv
from django.shortcuts import render
from django.http import HttpResponse
from core.models import TblTeam, TblDepartment, TblProject

def reports_dashboard(request):
    
    """
        Main Reports page
        Shows summary values and identifies teams missing a team leader
    """

    #Summary figures
    total_teams = TblTeam.objects.count()
    total_departments = TblDepartment.objects.count()
    total_projects = TblProject.objects.count()
    teams_no_leader = TblTeam.objects.filter(team_leader__isnull=True)

    #Store values
    context = {
        "total_teams": total_teams,
        "total_departments":total_departments,
        "total_projects":total_projects,
        "teams_no_leader": teams_no_leader,
    }

    return render(request, "reports/dashboard.html",context)

#def export_team_report_csv(request):
    #downloads team report with team summary
  #  response = HttpResponse(content_type="text/csv")
    #response[]