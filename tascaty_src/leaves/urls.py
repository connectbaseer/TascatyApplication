from django.urls import path
from .views import MyLeaves

urlpatterns = [
    path('leaves/', MyLeaves.as_view(), name='leaves'),
]
