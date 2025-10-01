from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    STATUS_CHOICES = (('todo', 'To Do'),('in_progress', 'In Progress'),('done', 'Done'),)

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')


    def __str__(self):
        return f"{self.title} ({self.assigned_to})"