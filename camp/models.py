from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.http import JsonResponse
from django.conf import settings



class User (AbstractUser):

    profile = models.TextField(default="Blank")
    points = models.CharField(max_length=10, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_TYPES = (
        ("1", "admin"),
        ("2", "teacher"),
        ("3", "leader"),
        ("4", "student")
    )

    status = models.CharField(max_length=5, choices=STATUS_TYPES, default=4)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
    REQUIRED_FIELDS = ['first_name', 'last_name', "status", "is_staff", "points", "profile"]

class Collective(models.Model):
    name = models.CharField(max_length=64)
    blockname = models.CharField(max_length=64)
    description = models.TextField()
    private = models.BooleanField()
    id_user = models.ForeignKey(to= settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator')
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through= 'MembersOfCollective',
        through_fields=('collective', 'user')
    )

class MembersOfCollective(models.Model):
    collective = models.ForeignKey(Collective, on_delete=models.CASCADE)
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


def __str__(self):
    return self.title