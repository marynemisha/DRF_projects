from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CountryDb(models.Model):
    country_name=models.CharField(max_length=100)
    country_code=models.IntegerField()


    def __str__(self):
        return self.country_name

class ApplicationDb(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(CountryDb, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=150)
    application_status = models.CharField(max_length=50, default="Pending")
    applied_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.course_name