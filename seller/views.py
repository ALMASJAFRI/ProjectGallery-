from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.decorators import is_seller
from seller.models import project,Category,project_detail
from django.contrib import messages
from django.contrib.auth import get_user_model
import threading
import zipfile
from django.conf import settings
from openai import OpenAI
User=get_user_model()
# Create your views here.
def is_valid_image(file):
    form_at=file.content_type
    if form_at not in ['image/jpeg','image/png']:
        return False
    return True
def is_zip(file):
    if not file.content_type=="application/zip":
        return False
    return True    
def unzip(path):
    ans={}
    content=""
    allowedext=".py"
    with zipfile.ZipFile(path,"r") as ref_ins:
        for file in ref_ins.namelist():
            if file.endswith(allowedext):
                content=ref_ins.read(file).decode("utf-8",errors="ignore")
                ans[file]=content 
    return ans
def AIenhance(id):
    try:
        ansstr = []
        item = project_detail.objects.filter(id=id).first()
        rawans = unzip(item.project_file.path)
        for name, content in rawans.items():
            ansstr.append(f"#{name}\n code:-{content}\n")
        ansstr = "".join(ansstr)

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.LLM_KEY,
            default_headers={
                "HTTP-Referer": "https://smartprojectgallery.onrender.com",
                "X-Title": "Smart Project Gallery",
            },
        )

        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "You are a great analyzer and assistant"},
                {"role": "user", "content": f"Analyze this code and list features only (no code):\n{ansstr}"}
            ],
            temperature=0,
        )

        feature = completion.choices[0].message.content
        item.features = feature
        item.save()
        print("✅ Features generated:", feature)

    except Exception as e:
        print("❌ AIenhance failed:", e)
    
                
@login_required
@is_seller
def sellerdash(request):   
    items=project_detail.objects.filter(project__user=request.user).order_by('-project__datein')
    return render(request,'seller/sellerboard.html',{'items':items})
@login_required 
@is_seller
def additem(request):
    if request.method=="POST":
        name=request.POST.get('item_name')
        description=request.POST.get('item_description')
        image=request.FILES.get('item_image')
        valid=is_valid_image(image)
        if not valid:
            messages.error(request,'image not valid')
            return render(request,'messages.html')
        price=request.POST.get('item_price')
        file=request.FILES.get('item_file')
        validate_file=is_zip(file)
        if not validate_file:
            messages.error(request,"file must be .zip format")
            return render(request,'messages.html')
        category=request.POST.get('item_category')
        document=request.FILES.get('document')
        cat=Category.objects.filter(cat_name=category).first()
        project_ins= project.objects.create(p_name=name,user=request.user)
        det_ins=project_detail.objects.create(project=project_ins,project_file=file,price=price,description=description,image=image,category=cat,project_document=document)
        #threading.Thread(target=AIenhance,args=(det_ins.id,)).start()
        AIenhance(det_ins.id)
        items=project_detail.objects.filter(project__user=request.user).order_by('-project__datein')
        return render(request,'partials/itemcard.html',{'items':items})
        
def features(request,id):
    item=project_detail.objects.filter(id=id).first()
    if not item.features:
        threading.Thread(target=AIenhance,args=(item.id,)).start()
        messages.error(request,"Please retry..")   
        return render(request,"partials/features.html",{'item':item})
    messages.success(request,"Features Updated")
    return render(request,"partials/features.html",{'item':item})    
        
        
        
    
