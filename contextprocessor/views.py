from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.http import HttpResponse

def Create_Superuser(request):
    User = get_user_model()
    # ✅ Change username, email, and password as you like
    username = 'Almasjafri'
    email = 'almas110@gmail.com'
    password = '12345'

    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(email=email, password=password)
        return HttpResponse("Superuser created successfully!")
    return HttpResponse("Superuser already exists.")
