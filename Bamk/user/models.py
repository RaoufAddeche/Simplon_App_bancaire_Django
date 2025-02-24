from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    advisor: Optional[str] = models.CharField(max_length=100, blank=True, null=True)
