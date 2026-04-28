from django.db import models
from core.models import TblTeam


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    meeting_link = models.URLField(max_length=500, blank=True)
    message = models.TextField(blank=True)
    team = models.ForeignKey(TblTeam, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
