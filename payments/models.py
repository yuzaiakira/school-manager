from django.db import models
from django_jalali.db.models import jDateField, jDateTimeField

from accounts.models import UserModel


# Create your models here.
class PayYearsModel(models.Model):
    date = jDateField(verbose_name="سال")

    class Meta:
        verbose_name_plural = "سال ها"
        verbose_name = "سال"

    def __str__(self):
        return str(self.date)


class TotalPriceModel(models.Model):
    year = models.ForeignKey(PayYearsModel, on_delete=models.CASCADE,
                             related_name="TotalPriceModel", verbose_name="سال",
                            )
    name = models.CharField(max_length=15, verbose_name="عنوان", null=True)
    price = models.BigIntegerField(verbose_name="شهریه کل")
    part = models.IntegerField(verbose_name="تعداد اقساط", default=0)

    class Meta:
        verbose_name_plural = "شهریه ها"
        verbose_name = "شهریه"

    def __str__(self):
        return "{} - {}".format(self.name, self.year)


class UserPriceModel(models.Model):
    total_price = models.ForeignKey(TotalPriceModel, on_delete=models.CASCADE,
                                    related_name="UserTotalPriceModel", verbose_name="شهریه", null=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,
                             related_name="UserPriceModel", verbose_name="کاربر", null=True)
    Installment = models.BooleanField(default=False, verbose_name="آیا قسطی بندی شود؟")
    finished = models.BooleanField(default=False, verbose_name="آیا شهریه کامل پرداخت شده؟")

    class Meta:
        verbose_name_plural = "شهریه کاربرها"
        verbose_name = "شهریه کاربر"

    def __str__(self):
        return "{} - {}".format(str(self.user), str(self.total_price))


class UserPaymentModel(models.Model):
    total = models.ForeignKey(UserPriceModel, on_delete=models.CASCADE,
                              related_name="UserPaymentModel", verbose_name="شهریه")
    date = jDateTimeField(verbose_name="تاریخ", null=True)
    price = models.BigIntegerField(verbose_name="مبلغ پرداختی", null=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)

    class Meta:
        verbose_name_plural = "پرداخت های کابران"
        verbose_name = "پرداخت کاربر"

    def __str__(self):
        return "{} {}".format(self.total.user.first_name, self.total.user.last_name)
