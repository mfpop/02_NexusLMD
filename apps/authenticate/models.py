from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import base64


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Store avatar as a base64 encoded string in the database
    avatar_data = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def avatar_url(self):
        """
        Returns a data URL for the avatar image.
        """
        if self.avatar_data:
            # Default to JPEG if no content type info is available
            return f"data:image/jpeg;base64,{self.avatar_data}"
        return None


class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_experiences')
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.company} - {self.position}"


class EducationExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education_experiences')
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.degree} at {self.institution}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile instance when a new User is created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Update the Profile instance when the User is updated"""
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except Profile.DoesNotExist:
        # Create a profile if it doesn't exist
        Profile.objects.create(user=instance)