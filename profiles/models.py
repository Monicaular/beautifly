from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    Represents a user profile containing default delivery information
    and order history. This model extends the built-in Django User model
    via a one-to-one relationship.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_full_name = models.CharField(
        max_length=50, null=False, blank=True
    )
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )
    default_country = CountryField(
        blank_label="Country *", null=True, blank=True
    )
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True
    )
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_county = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        """Return the username associated with this profile."""
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create a new user profile if a user is created,
    or update the existing profile for an existing user.
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
