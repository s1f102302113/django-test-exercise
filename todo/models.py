from django.db import models
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, default='')
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)  # メモフィールドを追加

    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt
