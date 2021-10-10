
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "TasCaty Admin"
admin.site.site_title = "TasCaty"
admin.site.index_title = "Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tascaty.urls')),
    path('', include('users.urls')),
    path('', include('leaves.urls')),
    path('', include('tascaty.api.urls')),
]

