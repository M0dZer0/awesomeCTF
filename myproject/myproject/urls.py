from django.urls import path
from myapp.views import beijing_time

urlpatterns = [
    path('beijing-time/', beijing_time, name='beijing_time'),
]
