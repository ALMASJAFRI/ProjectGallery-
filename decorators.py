from django.contrib import messages
from django.shortcuts import redirect
def is_seller(view_func):
    def wrapper(request,*args,**kwargs):
        user=request.user
        if user.is_authenticated and user.is_seller:
            return view_func(request,*args,**kwargs)
        messages.error(request,"You Are Not Allowed To Sell!")
        return redirect('/')
    return wrapper
    