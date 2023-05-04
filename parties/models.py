from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    Data_Subject = models.BooleanField('Data Subject', default=False)
    Requesting_party = models.BooleanField('Requesting Party', default=False)