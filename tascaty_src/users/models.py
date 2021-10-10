from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class team_leads(models.Model):
    user_name = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    full_name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.full_name


class tascaty_user(AbstractUser):
    is_team_lead = models.BooleanField(
        default=False, help_text="Designates if the user is having Team Lead Access")
    is_manager = models.BooleanField(
        default=False, help_text="Designates if the user is having Manager Access")
    approver = models.ForeignKey(
        team_leads, on_delete=models.DO_NOTHING, null=True, blank=True)

