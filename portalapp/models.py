# Models for Notice Management System - Updated by Chetan Kumar

from django.db import models
from django.contrib.auth.models import User

class Notice(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
