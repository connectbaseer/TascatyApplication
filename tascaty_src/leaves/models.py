from django.db import models
from users.models import team_leads
from tascaty.models import activity_status
from django.conf import settings
from django.urls import reverse 


class leaves(models.Model):
    user_name = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    approver = models.ForeignKey(
        team_leads, on_delete=models.DO_NOTHING, null=True)
    status = models.ForeignKey(
        activity_status, on_delete=models.DO_NOTHING, default=1)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    def get_absolute_url(self):
        return reverse('leaves')

