from django.db import models

# Create your models here.
class JobDb(models.Model):
    types=[
        ('Full Time','Full Time'),
        ('Part Time','Part Time'),
        ('Internship','Internship'),
        ('WFH','WFH'),
    ]
    job_types=models.CharField(max_length=100,choices=types)
    title=models.CharField(max_length=100)
    company_name=models.CharField(max_length=100)
    jd=models.TextField()
    location=models.CharField(max_length=100)
    salary=models.IntegerField()
    posted_data=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Applicant(models.Model):
    STATUS_CHOICES = [ 
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'), 
    ('Rejected', 'Rejected'),
    ]
    status=models.CharField(max_length=100,choices=STATUS_CHOICES)
    job=models.ForeignKey(JobDb,on_delete=models.CASCADE)
    applicant_name=models.CharField(max_length=100)
    email = models.EmailField() 
    phone = models.CharField(max_length=15) 
    qualification = models.CharField(max_length=100) 
    skills = models.TextField()
    applied_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.applicant_name


