from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class EventDb(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    event_date = models.DateField()
    location = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskDb(models.Model):
    event = models.ForeignKey(EventDb, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tasks")
    due_date = models.DateField()
    status = models.CharField(max_length=20,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class EventMemberDb(models.Model):
    event = models.ForeignKey(EventDb, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="joined_events")
    role = models.CharField(max_length=20, default='Member')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role