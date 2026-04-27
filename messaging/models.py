"""
Author: Marta Pikturnaite (w2073431)
"""
from django.db import models
from core.models import TblUser

class Message(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
    ]

    sender = models.ForeignKey(TblUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(TblUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.sender} to {self.recipient}"