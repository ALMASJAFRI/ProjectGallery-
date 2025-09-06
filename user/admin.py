from django.contrib import admin
from user.models import Variant,Cart,Cartitem,Order
# Register your models here.
class cartadmin(admin.ModelAdmin):
    list_display=['user','created']
    ordering=['user']
admin.site.register(Cart,cartadmin)
class Variantadmin(admin.ModelAdmin):
    list_display=['var_name']
admin.site.register(Variant,Variantadmin)
class cartitemadmin(admin.ModelAdmin):
    list_display=['cart','project','det','quantity','variant']
    ordering=['cart']
    list_filter=['cart','project','det','quantity','variant']
admin.site.register(Cartitem,cartitemadmin)

class Orderadmin(admin.ModelAdmin):
    list_display=['order_id','status','project','price']
    list_filter=['status','project','price']
    ordering=['status']
admin.site.register(Order,Orderadmin)

