from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class CategoryDb(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    category_type=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TransactionDb(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="transactions")
    category=models.ForeignKey(CategoryDb,on_delete=models.CASCADE,related_name="categories")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    transaction_type = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.name



