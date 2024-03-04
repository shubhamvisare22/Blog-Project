
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Model representing user profile information.

    Attributes:
        user (User): The associated User object.
        is_author (bool): Indicates whether the user is an author or not.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_author = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile for {self.user.username}"
