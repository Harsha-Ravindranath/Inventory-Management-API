"""
Custom user model for the application, extending Django's AbstractUser.
This model includes user types and a unique email field.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user class that extends AbstractUser to include additional fields.

    Attributes:
        user_type (str): Type of user, either 'Admin' or 'User'.
        email (str): Unique email address for the user.
    """
    
    user_type_choices = (
        ('Admin', 'Admin'),
        ('User', 'User'),
    )
    user_type = models.CharField(max_length=20, choices=user_type_choices,
                                 default='User', null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


