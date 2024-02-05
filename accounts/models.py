from django.db import models
from django.db.models import Q
from django.templatetags.static import static
from django.contrib.auth.models import AbstractUser

from django_jalali.db.models import jDateField

from accounts.functions import rename_profile_image


# Create your models here.
class StdGroupModel(models.Model):
    group_name = models.CharField(max_length=255, verbose_name="گروه", null=True)
    can_edit = models.BooleanField(default=True, verbose_name="اجازه ویرایش به این گروه میدهید؟")

    def __str__(self):
        return str(self.group_name)

    class Meta:
        verbose_name_plural = "کلاس ها"
        verbose_name = "کلاس"


class UserModel(AbstractUser):
    group = models.ForeignKey('StdGroupModel', related_name="StdGroupModel",
                              on_delete=models.CASCADE, verbose_name="سال ورودی دانش آموز",
                              blank=True, null=True)
    
    can_edit = models.BooleanField(default=False, verbose_name="اجازه ویرایش به این دانش آموز را میدهید؟")
    display_name = models.CharField(max_length=50, verbose_name="نام نمایشی در سایت", blank=True, null=True)
    profile_pic = models.ImageField(upload_to=rename_profile_image, default=None, null=True)

    class Meta:
        verbose_name_plural = "کاربران"
        verbose_name = "کاربر"
        permissions = [
            ("user_serach", "میتواند کاربران را جستجو و مشاهده کند"),
        ]

    def save(self, *args, **kwargs):
        if StdGroupModel.objects.exists():
            self.group = StdGroupModel.objects.last()
        else:
            self.group = None

        super().save(*args, **kwargs)

    @property
    def profile_pic_url(self):
        """Get picture form model if picture is null change by default picture
        you can use it in template
        """
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return static('assets/img/user.png')

    @property
    def site_display_name(self) -> str:
        """
        check display name if is none return first name or somthing else
        :return: str
        """
        if self.display_name:
            return self.display_name
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.username

    @property
    def user_group_name(self) -> str:
        """
        return user group name
        :return: str
        """
        try:
            return self.group.group_name
        except AttributeError:
            return ""

    @property
    def editable(self) -> bool:
        """
        check user can modify form or not
        :return: bool
        """
        return self.can_edit or self.group.can_edit


class StdReportModel(models.Model):
    student = models.ForeignKey('information.StdInfoModel', on_delete=models.CASCADE,
                                related_name="StdReportModel", verbose_name="دانش آموز")
    
    title = models.CharField(max_length=120, verbose_name="عنوان", null=True)
    desc = models.TextField(verbose_name="توضیحات", null=True)
    date = jDateField(verbose_name="تاریخ", null=True, blank=True)
    score = models.FloatField(verbose_name="نمره", blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "فعالیت های انضباطی"
        verbose_name = "فعالیت انضباطی"

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name}"
    
 
class StdEducationalBadModel(models.Model):
    title = models.CharField(max_length=120, verbose_name="عنوان", null=True)

    class Meta:
        verbose_name_plural = "موارد منفی انضباطی"
        verbose_name = "مورد منفی انضباطی"

    def __str__(self):
        return self.title
    
   
class StdEducationalGoodModel(models.Model):
    title = models.CharField(max_length=120, verbose_name="عنوان", null=True)
    
    class Meta:
        verbose_name_plural = "موارد مثبت انضباطی"
        verbose_name = "مورد مثبت انضباطی"
    
    def __str__(self):
        return self.title
    

class StdEducationalModel(models.Model):
    student = models.ForeignKey('information.StdInfoModel', on_delete=models.CASCADE,
                                related_name="StdEducationalModel", verbose_name="دانش آموز")
    
    good = models.ForeignKey('StdEducationalGoodModel', on_delete=models.CASCADE,
                             related_name="StdEducationalGoodModel",
                             verbose_name="موارد مثبت", null=True,
                             blank=True, default=None)
    
    bad = models.ForeignKey('StdEducationalBadModel', on_delete=models.CASCADE,
                            related_name="StdEducationalBadModel",
                            verbose_name="موارد منفی", null=True,
                            blank=True, default=None)
    
    number = models.IntegerField(verbose_name="تعداد", blank=True, null=True)
    score = models.FloatField(verbose_name="نمره", blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "پرونده های تربیتی "
        verbose_name = "پرونده تربیتی "

    def __str__(self):
        return f"برای {self.student.user.first_name} {self.student.user.last_name}"

    @classmethod
    def get_data(cls, student_id):
        return {
            'good': cls.objects.filter(Q(student=student_id) & Q(bad=None)),
            'bad': cls.objects.filter(Q(student=student_id) & Q(good=None)),
        }
    
    
