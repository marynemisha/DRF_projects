from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProjectDb(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    deadline=models.DateField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProjectMemberDb(models.Model):
    project=models.ForeignKey(ProjectDb,on_delete=models.CASCADE,related_name="project_details")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="project_members")
    joined_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=[models.UniqueConstraint(fields=['project','user'],name='unique_project_members')]


    def __str__(self):
        return f"{self.user.username} - {self.project.title}"
