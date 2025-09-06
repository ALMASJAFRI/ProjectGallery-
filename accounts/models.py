from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
class usermanager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("email is required")
        if not password:
            raise ValueError("password is neccessary for user")
        email=self.normalize_email(email=email)
        user=self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password=None,**extra_fields):
        user=self.create_user(email=email,password=password,**extra_fields)
        user.is_active=True
        user.is_staff=True
        user.is_seller=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
        

# Create your models here.
class Custom_User(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.IntegerField(null=True,blank=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    photo=models.FileField(upload_to="userpicture/",null=True,blank=True)
    token=models.CharField()
    is_staff=models.BooleanField(default=True)
    is_active=models.BooleanField(default=False)
    is_seller=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    objects=usermanager()
    USERNAME_FIELD='email'
REQUIRED_FIELDS=[]
def has_perm(self,perm,obj=None):
    return self.is_superuser
def has_module_perm(self,app_label):
    return self.is_superuser

    
    
