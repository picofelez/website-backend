from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    Customize user mode.
    """
    def __str__(self):
        return self.get_full_name()
