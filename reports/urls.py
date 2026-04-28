# Imports
from django.urls import path
from . import views

# List of urls which belong to the reports app
urlpatterns = [
    # when user visits /reports/ run reports_dashboard view.
    path("", views.reports_dashboard, name="reports_dashboard"),
    path("export/whole-report/", views.export_whole_report_csv, name="export_whole_report_csv"),
    path("export/department-report/", views.export_department_report_csv, name="export_department_report_csv"),
    path("export/project-report/", views.export_project_report_csv, name="export_project_report_csv"),
    path("export/dependency-report/", views.export_dependency_report_csv, name="export_dependency_report_csv"),
    path("visualisations/", views.visualisations_view, name="reports_visualisations"),
]
