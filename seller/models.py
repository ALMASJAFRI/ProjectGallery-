from django.db import models
# Create your models here.
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.contrib.auth import get_user_model
User=get_user_model()
class Category(models.Model):
    cat_name=models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural="Categories"
    def __str__(self):
        return self.cat_name
class project(models.Model):
    p_name=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    in_stock=models.BooleanField(default=True)
    datein=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.p_name
class project_detail(models.Model):
    project=models.ForeignKey(project,on_delete=models.CASCADE)
    project_file=models.FileField(upload_to="projects/",storage=RawMediaCloudinaryStorage(),null=True,blank=True)
    project_document=models.FileField(upload_to='project_document',storage=RawMediaCloudinaryStorage(),null=True,blank=True) 
    price=models.IntegerField()
    description=models.TextField()
    features=models.TextField(null=True,blank=True)
    #image=models.FileField(upload_to='project_img')
    image=CloudinaryField('image',null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    purchased=models.IntegerField(default=0.0,null=True,blank=True)
    

    
