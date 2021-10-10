from django.contrib import admin
from .models import activity, system, client, activity_status

admin.site.register(activity)
admin.site.register(system)
admin.site.register(client)
admin.site.register(activity_status)