"""
URL configuration for Projectgallery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from user import views as us
from seller import views as sel
from accounts import views as acc
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",us.home,name="home"),
    path('login_page/',acc.login_page,name='login_page'),
    path('register/',acc.register,name='register'),
    path('cart/',us.cart,name="cart"),
    path('sellerdas/',sel.sellerdash,name="sellerdash"),
    path('additem/',sel.additem,name="additem"),
    path('activate/<token>/',acc.activate,name="activate"),
    path('search/',us.search,name="search"),
    path('searchsell/',us.searchsell,name="searchsell"),
    path('detail/<id>/',us.details,name="detail"),
    path('price_differ/<id>/',us.price_var,name="price_differ"),
    path('reviewadd/<id>/',us.reviewadd,name="review"),
    path('addtocart/<id>/',us.addcart,name="addtocart"),
    path('removefromcart/<id>/',us.removecart,name="removefromcart"),
    path('initiateorder/<id>/<price>/',us.inititate,name="initiateorder"),
    path('successtrue/',us.validatepay,name="successtrue"),
    path('failedtrue/',us.validatepay,name="failedtrue"),
    path('test/',us.test,name="test"),
    path('logout/',acc.logoutpage,name="log_out"),
    path('featurea/<id>/',sel.features,name="features"),
    path('about/',acc.about,name="about_us"),
    path('contact/',acc.contact,name="contact_us"),
    path('profile/',acc.profile,name="profile"),
    path('changephoto/',acc.changephoto,name="uploadphoto")
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

