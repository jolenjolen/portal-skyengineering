from django.db import models


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    meeting_link = models.URLField(max_length=500, blank=True)  # optional — not all meetings have a link

    def __str__(self):
        return self.title
