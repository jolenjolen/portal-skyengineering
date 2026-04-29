from django.urls import path
from . import views

app_name = 'organisation'

urlpatterns = [
    path('', views.organisation_overview, name='overview'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:dept_id>/', views.department_detail, name='department_detail'),
    path('org-chart/', views.org_chart, name='org_chart'),
    path('dependencies/', views.dependencies_view, name='dependencies'),
    path('team-types/', views.team_type_view, name='team_types'),
]