from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
User=get_user_model()
def is_seller(view_func):
    def wrapper(request,*args,**kwargs):
        user=request.user
        if user.is_authenticated and user.is_seller:
            return view_func(request,*args,**kwargs)
        messages.error(request,"You Are Not Allowed To Sell!")
        return redirect('/')
    return wrapper
    