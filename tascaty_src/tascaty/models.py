from django.db import models
from django.conf import settings
from users.models import team_leads
from django.urls import reverse


class activity(models.Model):
    activity_name = models.CharField(max_length=200)

    def __str__(self):
        return self.activity_name


class system(models.Model):
    system_name = models.CharField(max_length=100)

    def __str__(self):
        return self.system_name


class client(models.Model):
    client_name = models.CharField(max_length=100)

    def __str__(self):
        return self.client_name


class activity_status(models.Model):
    status_name = models.CharField(max_length=20)

    def __str__(self):
        return self.status_name


class activity_tracker(models.Model):
    activity_name = models.ForeignKey(
        activity, on_delete=models.DO_NOTHING, null=False)
    system_name = models.ForeignKey(
        system, on_delete=models.DO_NOTHING, null=False)
    client_name = models.ForeignKey(
        client, on_delete=models.DO_NOTHING, null=False)
    hours = models.IntegerField(null=True)
    mins = models.IntegerField(null=True)
    no_of_records = models.IntegerField(null=True)
    date = models.DateField(null=False)
    project_id = models.TextField(null=True,blank=True)
    user_comments = models.TextField(null=True,blank=True)
    user_name = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(
        activity_status, on_delete=models.DO_NOTHING, default=1)
    approver = models.ForeignKey(team_leads, on_delete=models.DO_NOTHING, null=True)



    def get_absolute_url(self):
        return reverse('mytask')
