from django.db import transaction
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMessage
import hashlib 
import uuid
import threading
from decimal import Decimal
# Create your views here
from seller.models import project_detail,project,Category
from user.models import Review,Cartitem,Cart,Order
def home(request):
    items=project_detail.objects.all().order_by('-project__datein')
    return render(request,"user/home.html",{'items':items})
def details(request,id):
    item=project_detail.objects.filter(id=id).first()
    rev=Review.objects.filter(project=item.project).order_by('-id')
    if not item:
        messages.error(request,"Project not found!!")
        return redirect("/")
    return render(request,'user/detail.html',{'item':item,'reviews':rev})
@login_required
def cart(request):
    items=Cartitem.objects.filter(cart__user=request.user)
    total=0
    total_items=0
    for item in items:
        total+=item.det.price
        total_items+=1  
    return render(request,'user/cart.html',{'items':items,'total':total,'total_items':total_items})
@login_required
def addcart(request,id):
    if request.method=="GET":
        detins=project_detail.objects.filter(id=id).first()
        projectins=detins.project
        if not projectins or not detins :
            messages.error(request,"Project not found")
            return render(request,'messages.html')
        cart,created=Cart.objects.get_or_create(user=request.user)
        cartitem_ins=Cartitem.objects.create(project=projectins,det=detins,cart=cart)
        cartitem_ins.quantity+=1
        cartitem_ins.save()
        messages.success(request,"Item Added To Wished")
        return render(request,'messages.html')
    return HttpResponse("bad request 404")
        
def search(request):
    if request.method=="GET":
        element=request.GET.get('element')
        items=project_detail.objects.filter(Q(project__p_name__icontains=element)|Q(price__icontains=element)|Q(description__icontains=element)|Q(category__cat_name__icontains=element)).order_by('-project__datein')
        return render(request,"partials/itemcard.html",{"items":items})
    return HttpResponse("bad request 404")
def searchsell(request):
    if request.method=='GET':
        element=request.GET.get('element')
        user=request.user
        items=project_detail.objects.filter((Q(project__user=user)&(Q(project__p_name__icontains=element)|Q(price__icontains=element)|Q(description__icontains=element)|Q(category__cat_name__icontains=element)))).order_by('-project__datein')
        return render(request,"partials/itemcard.html",{"items":items})
    return HttpResponse("bad request 404")
def price_var(request,id):
    det=project_detail.objects.filter(id=id).first()
    price=det.price
    if request.method=="POST":
        var=request.POST.get('var')
        if not var:
            messages.error(request,"variant not available")
            return redirect("detail")
        if var=="DOC+CODE":
            return render(request,"partials/price.html",{'price':price,'item':det})
        elif var=="ONLY CODE":
            new_price=0
            new_price=price-(price*(25/100))
            return render(request,"partials/price.html",{'price':new_price,'item':det})
        else :
            new_price=0
            new_price=price-(price*(75/100))
            return render(request,"partials/price.html",{'price':new_price,'item':det})
    return HttpResponse("bad request 404")
@login_required
def reviewadd(request,id):
    if request.method=="POST":
        review=request.POST.get('review')
        det=project_detail.objects.filter(id=id).first()
        projectins=det.project
        Review.objects.create(user=request.user,project=projectins,review=review)
        rev=Review.objects.filter(project=projectins).order_by('-id')
        messages.success(request,"review added")
        return render(request,'partials/reviews.html',{'reviews':rev})
@login_required
def removecart(request,id):
    if request.method=='GET':
        Cartitem.objects.filter(id=id).delete()
        items=Cartitem.objects.filter(cart__user=request.user)
        total=0
        total_items=0
        for item in items:    
            total+=item.det.price
            total_items+=1
        messages.success(request,"Item Removed")
        return render(request,'partials/cartitems.html',{'items':items,'total':total,'total_items':total_items})
def traxid():
    txid=str(uuid.uuid4())
    print(txid)
    return txid
@login_required
def inititate(request,id,price):
    print("DEBUG:", str)
    detins=project_detail.objects.filter(id=id).first()
    project_ins=detins.project
    if not project_ins or not detins:
        messages.error(request,"Project not found try again !!")
        return render(request,"user/home.html")
    user=request.user
    order,created=Order.objects.get_or_create(project=project_ins,det=detins,user=user)
    txnid=traxid()
    order.order_id=txnid
    order.save()
    email=user.email
    first_name=user.first_name or 'monti'
    phone=user.phone or "9999999999"
    price=Decimal(price)
    price=f"{price:.2f}"
    print("price",price)
    order.price=price
    order.save()
    productinfo=project_ins.p_name
    print("initiatte:-",productinfo)
    udf1 = udf2 = udf3 = udf4 = udf5 = ""
    hash_str=f"{settings.PAYU_KEY}|{txnid}|{price}|{productinfo}|{first_name}|{email}|{udf1}|{udf2}|{udf3}|{udf4}|{udf5}||||||{settings.PAYU_SALT}"
    hashh = hashlib.sha512(hash_str.encode('utf-8')).hexdigest().lower()
    order.hashs=hashh
    order.save()
    print('hadhstr',hash_str)
    print('hashh',hashh)
    data={'key':settings.PAYU_KEY,'email':email,'phone':phone,'firstname':first_name,'txnid':txnid,'amount':price,'productinfo':productinfo,'hash':hashh,'surl':'https://smartprojectgallery.onrender.com/successtrue/','furl':'https://smartprojectgallery.onrender.com/failedtrue/','item':detins}
    return render(request,'user/paymentinitiate.html',data)
@csrf_exempt
def validatepay(request):
    if request.method== 'POST' and 'status' in request.POST:
        txnid=request.POST.get('txnid')
        first_name=request.POST.get('firstname')
        email=request.POST.get('email')
        productinfo=request.POST.get('productinfo')
        amount=request.POST.get('amount')
        order=Order.objects.filter(order_id=txnid).first()
        if not order:
            messages.error(request,"order dosent exist")
            return redirect('home')
        if not order.order_id==txnid:
            messages.error(request,"transaction id did not match!!")
            return redirect('home')
        status=request.POST.get('status')
        if status=="success":
            mihpayid=request.POST.get("mihpayid")
            order.payu_payment_id=mihpayid
            order.status=True
            order.save()
            projectins=project_detail.objects.filter(project__p_name=productinfo).first()
            #t=threading.Thread(target=sendfiles,args=(amount,projectins.id,email))
            #t.start()
            sendfiles(amount,projectins.id,email)
            messages.success(request,"Payment Done")
            data={'txnid':txnid,'email':email,'product':productinfo,'amount':amount,'paymentid':mihpayid}
            return render(request,"accounts/successpage.html",data)
        else:
            messages.error(request,"Payment Failed!!")
            order.status=False
            order.save()
            data={'txnid':txnid,'email':email,'product':productinfo,'amount':amount,'paymentid':mihpayid,}
            return render(request,"accounts/failpage.html",data)
    return HttpResponse("bad request 404")
def sendfiles(price,id,email):
    try:
        price = Decimal(price)
        subject = "Purchase successful !!"
        from_email = "djangoprojects954@gmail.com"
        to = [email]
        message = ""
        projectins = project_detail.objects.get(id=id)
        codefile = projectins.project_file
        doc = projectins.project_document
        amount = Decimal(projectins.price)
        print("doc", doc.size)
        print("code", codefile.size)
        print('price', price)
        print('amount', amount)
        docurl = doc.url
        codeurl = codefile.url 

        if abs(price - amount) < Decimal('0.01'):
            message = f"Download Your Files Here.\n Document:http://127.0.0.1:8000/{docurl} \n Code:http://127.0.0.1:8000/{codeurl}"
            email_sent = EmailMessage(subject=subject, body=message, from_email=from_email, to=to)
            email_sent.send()
            print("sent")
        elif abs(price - (amount * Decimal('0.25'))) < Decimal('0.01'):
            message = f"Download Your Files Here. \n Code:http://127.0.0.1:8000/{codeurl}"
            email_sent = EmailMessage(subject=subject, body=message, from_email=from_email, to=to)
            email_sent.send()
            print("sent")
        elif abs(price - (amount * Decimal('0.75'))) < Decimal('0.01'):
            message = f"Download Your Files Here. \n Document:http://127.0.0.1:8000/{docurl}"
            email_sent = EmailMessage(subject=subject, body=message, from_email=from_email, to=to)
            email_sent.send()
            print("sent")
        else:
            print("No Variant Found")
    except Exception as e:
        print("⚠️ Error in sending email:", str(e))
        
        
def test(request):
    cat=request.GET.get('category')
    Category.objects.create(cat_name=cat)
    messages.success(request,"Category added!!")
    return render(request,"user/home.html")    
                
            
        
      
