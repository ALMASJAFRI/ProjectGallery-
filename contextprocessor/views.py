from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.http import HttpResponse

def create_superuser(request):
    User = get_user_model()
    # ✅ Change username, email, and password as you like
    username = 'Almasjafri'
    email = 'djangoprojects954@gmail.com'
    password = '12345'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        return HttpResponse("Superuser created successfully!")
    return HttpResponse("Superuser already exists.")
