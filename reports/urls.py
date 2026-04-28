# Imports
from django.urls import path
from . import views

# List of urls which belong to the reports app
urlpatterns = [
    # when user visits /reports/ run reports_dashboard view.
    path("", views.reports_dashboard, name="reports_dashboard"),
    path("export/csv/", views.export_team_report_csv, name="export_team_report_csv"),
    path("visualisations/", views.visualisations_view, name="reports_visualisations"),
]
