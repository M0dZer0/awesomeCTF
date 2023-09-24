from django.shortcuts import render
from .models import zrq

def zrqView(request):
    all_zrq = zrq.objects.all()
    return render(request, 'intro.html', {'zrq': all_zrq})

def intro(request):
    return render(request, 'intro.html')