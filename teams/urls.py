from django.urls import path
from .views import team_list_view, team_detail_view, team_schedule_meeting_view

urlpatterns = [
    path('', team_list_view, name='team_list'),
    path('<int:team_id>/', team_detail_view, name='team_detail'),
    path('<int:team_id>/schedule/', team_schedule_meeting_view, name='team_schedule_meeting'),
]
