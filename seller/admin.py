from django.contrib import admin
from seller.models import project,project_detail,Category
class categoryadmin(admin.ModelAdmin):
    list_display=['cat_name']
admin.site.register(Category,categoryadmin)
class projectadmin(admin.ModelAdmin):
    list_display=['p_name','user','in_stock']
    search_fields=['user']
# Register your models here.
admin.site.register(project,projectadmin)
class projectdetail(admin.ModelAdmin):
    search_fields=['project']
    list_display=['project','price','category','project_file','project_document']
admin.site.register(project_detail,projectdetail)

