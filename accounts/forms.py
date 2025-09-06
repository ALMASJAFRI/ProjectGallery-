from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Custom_User
class usercreationform(UserCreationForm):
    class Meta:
        model=Custom_User
        fields=['email','phone','name','password','is_seller','photo','first_name','last_name']
class userupdateform(UserChangeForm):
    class Meta:
        model=Custom_User
        fields=['name','phone','first_name','last_name','photo','first_name','last_name']
        