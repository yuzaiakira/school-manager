from django.db import models
from django_jalali.db.models import jDateField
from accounts.models import UserModel
from blog.functions import path_and_rename

class PostModel(models.Model):
    title = models.CharField(verbose_name="عنوان", max_length=120)
    content = models.TextField(verbose_name="محتوا")
    pic = models.ImageField(upload_to=path_and_rename, default=None, blank=True, null=True )
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="نویسنده")
    updated_on = jDateField(auto_now= True)
    created_on = jDateField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"

    def __str__(self):
        return self.title


