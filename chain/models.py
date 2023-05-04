from django.db import models

# Create your models here.
from django.db import models

class Request(models.Model):
    Rqp_name = models.CharField(max_length=100)
    Ds_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

class Token(models.Model):
    signature = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.signature} - {self.receiver} - {self.token} - {self.expiry_date}"