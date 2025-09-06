import threading 
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,get_user_model,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid
from django.core.mail import send_mail
User=get_user_model()

# Create your views here.
def register(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        name=request.POST.get('name')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        status=request.POST.get('status')
        phone=request.POST.get('phone')
        if User.objects.filter(email=email).first():
            messages.error(request,"email already exists")
            return render(request,'messages.html')
        if not email:
            messages.error(request,"Email is required")
            return render(request,'messages.html')
        if not password:
            messages.error(request,"password is required")
            return render(request,'messages.html')
        user=User.objects.create_user(email=email,password=password)
        user.first_name=first_name
        user.last_name=last_name
        user.name=name
        if phone:
            user.phone=int(phone)
        if status=='seller':
            user.is_seller=True
        token=str(uuid.uuid4())
        user.token=token
        user.save()
        messages.success(request,"email sent")
        threading.Thread(target=sendmail,args=(email,token)).start()
        return render(request,'messages.html')
    return render(request,'accounts/register.html')
        
def sendmail(email,token):
    subject="Request To Activate Account....!"
    message = f"Please Verify Your Email\n click here https://smartprojectgallery.onrender.com/activate/{token}/"
    from_email="djangoprojects954@gmail.com"
    recipient_list=[email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,fail_silently=False) 
def activate(request,token):
    user=User.objects.filter(token=token).first()
    if user:
        user.is_active=True
        user.save()
        messages.success(request,"Account Activated Login now!")
        return redirect('/')
    else:
        messages.error(request,"Account Activation Failed! Please Register Again")
        return redirect('/')
def login_page(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        name=request.POST.get('name')
        if not email:
            messages.error(request,"email is not valid")
            return render(request,'messages.html')
        if not password:
            messages.error(request,"password is required")
            return render(request,'messages.html')
        user=authenticate(request,email=email,password=password)
        if not user:
            messages.error(request,"invalid credentials")
            return render(request,'messages.html')
        login(request,user)
        messages.success(request,"login successful!!")
        return redirect('home')
    return render(request,'accounts/login.html')
@login_required
def logoutpage(request):
    user=request.user
    logout(request)
    messages.success(request,"Log Out successfull!!")
    return redirect("/")
    
def about(request):
    return render(request,"accounts/about.html")
def contact(request):
    return render(request,"accounts/contact.html")
@login_required
def profile(request):
    user=request.user
    return render(request,"accounts/profile.html",{'data':user})
def validateimg(image):
    whatis=image.content_type
    valid=["image/jpeg","image/png"]
    if whatis not in valid:
        return False
    return True        
@login_required
def changephoto(request):
    if request.method=="POST":
        image=request.FILES.get('photo')
        if not validateimg(image):
            data=request.user
            messages.error(request,"file must be image")
            return render(request,"partials/photo.html",{'data':data})
        request.user.photo=image
        request.user.save()
        data=request.user
        messages.success(request,"image updated")
        return render(request,"partials/photo.html",{'data':data})
   

    
