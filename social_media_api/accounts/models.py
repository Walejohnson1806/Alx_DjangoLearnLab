
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/images', blank=True, null=True)

    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following_users',
        blank=True # Differentiates the reverse relation
    )

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers_users'  # Differentiates the reverse relation
    )

    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow another user."""
        self.following.add(user)

    def unfollow(self, user):
        """Unfollow another user."""
        self.following.remove(user)

    def is_following(self, user):
        """Check if the user is following another user."""
        return self.following.filter(id=user.id).exists()
    
    def __str__(self):
        return self.username
