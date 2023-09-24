from django.contrib import admin
from django.urls import path, include
from intro_page.views import zrqView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('intro_page.urls')),
    path('zrq/', zrqView, name='zrq'),
]
