from django.db import models
from django.urls import reverse
from django.templatetags.static import static

from django_jalali.db.models import jDateField

from accounts.models import UserModel
from blog.functions import path_and_rename



class PostModel(models.Model):
    title = models.CharField(verbose_name="عنوان", max_length=120)
    content = models.TextField(verbose_name="محتوا")
    pic = models.ImageField(verbose_name="تصویر", upload_to=path_and_rename, default=None, blank=True, null=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="نویسنده")
    updated_on = jDateField(verbose_name="آخرین ویرایش", auto_now=True)
    created_on = jDateField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog-detail', args=[str(self.id)])

    @property
    def get_pic_url(self):
        """Get picture form model if picture is null change by default picture
        you can use it in template
        """
        if self.pic and hasattr(self.pic, 'url'):
            return self.pic.url
        else:
            return static('assets/img/no-image.png')

