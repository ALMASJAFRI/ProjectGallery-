from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.forms import usercreationform,userupdateform
from accounts.models import Custom_User

class customadmin(UserAdmin):
    model=Custom_User
    add_form=usercreationform
    form=userupdateform
    list_display=['email','name','is_active','is_seller',]
    search_fields=('email','is_active',)
    ordering=('email',)
    fieldsets=[('informaion',{'fields':('email','phone','password','name','photo','first_name','last_name')}),
        ('status',{'fields':('is_active','is_staff','is_seller')}),]
admin.site.register(Custom_User,customadmin)
    

# Register your models here.
