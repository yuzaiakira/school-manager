from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django_jalali.db.models import jDateField
from multiselectfield import MultiSelectField
# Create your models here.


class StdInfoModel(models.Model):
    user = models.OneToOneField('accounts.UserModel', on_delete=models.CASCADE, related_name="StdInfoModel",
                                verbose_name="دانش آموز")

    id_code = models.CharField(max_length=10, verbose_name="کد ملی", null=True, )

    certificate_place = models.CharField(max_length=20, verbose_name="محل صدور شناسنامه", null=True)
    certificate_Zone = models.CharField(max_length=20, verbose_name="حوزه صدور", null=True)
    serial = models.CharField(max_length=6, verbose_name="سریال", null=True)
    serial_number = models.CharField(max_length=3, verbose_name="عدد سری", null=True)
    serial_char = models.CharField(max_length=3, verbose_name="حرف سری", null=True)

    birth_place = models.CharField(max_length=20, verbose_name="محل تولد", null=True)
    birthday = jDateField(verbose_name="تاریخ تولد", null=True)

    status_choices = ((1, "سالم"),
                      (2, "معلول"),
                      (3, "بیماری خاص"))

    physical_condition = models.IntegerField(choices=status_choices,
                                             verbose_name="وضعیت جسمانی",
                                             null=True)
    status_hands = (('r', "راست دست"),
                    ('l', "چپ دست"))
    hands = models.CharField(choices=status_hands, max_length=1, verbose_name="چپ دست/ راست دست", null=True)

    special_Des = models.CharField(max_length=30, verbose_name="توضیحات بیماری خاص", blank=True, null=True)

    family_size = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)],
                                      verbose_name="تعداد خانواده", null=True)

    child_num = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)],
                                    verbose_name="فرزند چندم؟", null=True)

    bro_num = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)],
                                  verbose_name="تعداد برادر", null=True)

    sis_num = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)],
                                  verbose_name="تعداد خواهر", null=True)

    status_place = (
        (1, 'شخصی'),
        (2, 'اجاره'),
        (3, 'سازمانی'),
        (4, 'سایر')
    )

    place = models.IntegerField(choices=status_place, verbose_name="وضعیت مسکن خانواده", null=True)

    status_live = (
        (1, 'پدر و مادر'),
        (2, 'پدر و مادر خوانده'),
        (3, 'مادر و پدر خوانده'),
        (4, 'پدر'),
        (5, 'مادر'),
        (6, 'پدر بزرگ و یا مادر بزرگ'),
        (7, 'سایر بستگان'),
    )
    live_with = models.IntegerField(choices=status_live, verbose_name="در خانواده با چه کسی زندگی میکند؟", null=True)

    status_Insurance = (
        (0, 'هیچ کدام'),
        (1, 'امداد'),
        (2, 'بهزیستی'),
        (3, 'فرزند شهید'),
        (4, 'فرزند مفقودالاثر'),
        (5, 'فرزنده آزاده'),
        (6, 'فرزند جانباز'),
    )
    insurance = models.IntegerField(choices=status_Insurance, verbose_name="تحت پوشش کدام کمیته هستید؟", null=True)

    veteran_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                             verbose_name="درصد جانبازی", blank=True, null=True)

    sacrifice_code = models.CharField(max_length=10, verbose_name="کد ایثارگری", blank=True, null=True)
    legal_guardian = models.CharField(max_length=100, verbose_name="سرپرست قانونی", null=True)
    legal_guardian_id = models.CharField(max_length=10, verbose_name="کد ملی سرپرست", null=True)

    class Meta:
        verbose_name_plural = "مشخصات دانش آموز ها"
        verbose_name = "مشخصات دانش آموز"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class FatherInfoModel(models.Model):
    student = models.OneToOneField('StdInfoModel', on_delete=models.CASCADE,
                                   related_name="FatherInfoModel", verbose_name="دانش آموز")

    first_name = models.CharField(max_length=20, verbose_name="نام", null=True)
    last_name = models.CharField(max_length=20, verbose_name="نام خانوادگی", null=True)
    certificate_num = models.CharField(max_length=10, verbose_name="شماره شناسنامه", null=True)
    birthday = jDateField(verbose_name="تاریخ تولد", null=True)
    id_code = models.CharField(max_length=10, verbose_name="کد ملی", null=True)
    certificate_place = models.CharField(max_length=20, verbose_name="محل صدور", null=True)

    is_dead_status = (
        (0, 'هیچ کدام'),
        (1, 'فوت کرده است'),
        (2, 'شهید')
    )
    is_dead = models.IntegerField(choices=is_dead_status, verbose_name="وضعیت پدر", null=True)
    marital_status = (
        (0, 'متاهل'),
        (1, 'مجرد'),
        (2, 'طلاق')
    )
    marital = models.IntegerField(choices=marital_status, verbose_name="وضعیت تاهل", null=True)

    education = models.CharField(max_length=30, verbose_name="مدرک و رشته تحصیلی", null=True)
    work_status = (
        (0, 'بخش دولتی'),
        (1, 'خصوصی'),
        (2, 'آزاد'),
        (3, 'سایر'),
    )
    work = models.IntegerField(choices=work_status, verbose_name="شاغل در", null=True)
    work_name = models.CharField(max_length=10, verbose_name="عنوان شغلی", null=True)
    work_place = models.CharField(max_length=30, verbose_name="محل کار", null=True)

    cooperation_status = (
        ("0", 'مایل به همکاری نیستم'),
        ("1", 'عمران و فنی'),
        ("2", 'برگزاری مراسم ها و برنامه های مدرسه'),
        ("3", 'تجهیز مدرسه'),
        ("4", 'متناسب با شغل و تخصص'),
    )
    cooperation = MultiSelectField(max_length=5, choices=cooperation_status, verbose_name="زمینه های همکاری", null=True)
    cooperation_des = models.CharField(max_length=30, verbose_name="توضیح بیشتر", blank=True, null=True)

    class Meta:
        verbose_name_plural = "مشخصات پدران دانش آموزان"
        verbose_name = "مشخصات پدر دانش آموز"

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name}"


class MatherInfoModel(models.Model):
    student = models.OneToOneField('StdInfoModel', on_delete=models.CASCADE,
                                   related_name="MatherInfo", verbose_name="دانش آموز")

    first_name = models.CharField(max_length=20, verbose_name="نام", null=True)
    last_name = models.CharField(max_length=20, verbose_name="نام خانوادگی", null=True)
    certificate_num = models.CharField(max_length=10, verbose_name="شماره شناسنامه", null=True)
    birthday = jDateField(verbose_name="تاریخ تولد", null=True)
    id_code = models.CharField(max_length=10, verbose_name="کد ملی", null=True)

    is_dead_status = (
        (0, 'هیچ کدام'),
        (1, 'فوت کرده است'),
        (2, 'شهید')
    )
    is_dead = models.IntegerField(choices=is_dead_status, verbose_name="وضعیت مادر", null=True)
    marital_status = (
        (0, 'متاهل'),
        (1, 'مجرد'),
        (2, 'طلاق')
    )
    marital = models.IntegerField(choices=marital_status, verbose_name="وضعیت تاهل", null=True)

    education = models.CharField(max_length=30, verbose_name="مدرک و رشته تحصیلی", null=True)
    work_status = (
        (0, 'بخش دولتی'),
        (1, 'خصوصی'),
        (2, 'آزاد'),
        (3, 'سایر'),
    )
    work = models.IntegerField(choices=work_status, verbose_name="شاغل در", null=True)
    work_name = models.CharField(max_length=10, verbose_name="عنوان شغلی", null=True)
    work_place = models.CharField(max_length=30, verbose_name="محل کار", null=True)

    cooperation_status = (
        (0, 'مایل به همکاری نیستم'),
        (1, 'عمران و فنی'),
        (2, 'برگزاری مراسم ها و برنامه های مدرسه'),
        (3, 'تجهیز مدرسه'),
        (4, 'متناسب با شغل و تخصص'),
    )
    cooperation = MultiSelectField(choices=cooperation_status,
                                   verbose_name="زمینه های همکاری", null=True)

    cooperation_des = models.CharField(max_length=30, verbose_name="توضیح بیشتر",
                                       blank=True, null=True)

    class Meta:
        verbose_name_plural = "مشخصات مادران دانش آموزان"
        verbose_name = "مشخصات مادر دانش آموز"

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name}"


class SupervisorInfoModel(models.Model):
    student = models.OneToOneField('StdInfoModel', on_delete=models.CASCADE,
                                   related_name="SupervisorInfoModel", verbose_name="دانش آموز")

    first_name = models.CharField(max_length=20, verbose_name="نام", blank=True, null=True)
    last_name = models.CharField(max_length=20, verbose_name="نام خانوادگی", blank=True, null=True)
    certificate_num = models.CharField(max_length=10, verbose_name="شماره شناسنامه", blank=True, null=True)

    birthday = jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    id_code = models.CharField(max_length=10, verbose_name="کد ملی", blank=True, null=True)
    certificate_place = models.CharField(max_length=20, verbose_name="محل صدور", null=True)
    relationship = models.CharField(max_length=20, verbose_name="نسبت با دانش آموز",
                                    blank=True, null=True)

    marital_status = (
        (0, 'متاهل'),
        (1, 'مجرد'),
        (2, 'طلاق')
    )
    marital = models.IntegerField(choices=marital_status, verbose_name="وضعیت تاهل",
                                  blank=True, null=True)

    education = models.CharField(max_length=30, verbose_name="مدرک و رشته تحصیلی", blank=True,
                                 null=True)
    work_status = (
        (0, 'بخش دولتی'),
        (1, 'خصوصی'),
        (2, 'آزاد'),
        (3, 'سایر'),
    )
    work = models.IntegerField(choices=work_status, verbose_name="شاغل در", blank=True, null=True)
    work_name = models.CharField(max_length=10, verbose_name="عنوان شغلی", blank=True, null=True)
    work_place = models.CharField(max_length=30, verbose_name="محل کار", blank=True, null=True)

    cooperation_status = (
        (0, 'مایل به همکاری نیستم'),
        (1, 'عمران و فنی'),
        (2, 'برگزاری مراسم ها و برنامه های مدرسه'),
        (3, 'تجهیز مدرسه'),
        (4, 'متناسب با شغل و تخصص'),
    )
    cooperation = MultiSelectField(choices=cooperation_status, verbose_name="زمینه های همکاری",
                                   blank=True, null=True)

    cooperation_des = models.CharField(max_length=30, verbose_name="توضیح بیشتر", blank=True,
                                       null=True)

    class Meta:
        verbose_name_plural = "مشخصات سرپرستان دانش آموزان"
        verbose_name = "مشخصات سرپرست دانش آموز"

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name}"


class StdLastSchoolModel(models.Model):
    student = models.OneToOneField('StdInfoModel', on_delete=models.CASCADE,
                                   related_name="StdLastSchoolModel", verbose_name="دانش آموز")

    last_school = models.CharField(max_length=20, blank=True, verbose_name="نام مدرسه سال قبلی",
                                   null=True)

    last_city = models.CharField(max_length=20, blank=True, verbose_name="شهرستان", null=True)
    phone = models.CharField(max_length=15, blank=True, verbose_name="تلفن مدرسه", null=True)
    score = models.CharField(max_length=5, blank=True, verbose_name="معدل کل", null=True)

    class Meta:
        verbose_name_plural = "اطلاعات تحصیلی دانش آموزان"
        verbose_name = "اطلاعات تحصیلی دانش آموز"

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name}"


class StdCompetitionsModel(models.Model):
    student = models.OneToOneField('StdInfoModel', on_delete=models.CASCADE,
                                   related_name="StdCompetitionsModel", verbose_name="دانش آموز")
    quranic_status = (
        (1, 'قرائت'),
        (2, 'حفظ کل'),
        (3, 'حفظ جزء'),
        (4, 'مداحی'),
        (5, 'نحج البلاغه'),
        (6, 'احکام'),
        (7, 'انشای نماز'),
        (8, 'صحیفه سجادیه'),
        (9, 'اذان'),
    )
    quranic = MultiSelectField(choices=quranic_status,
                               verbose_name="در کدام زمینه قرآنی و مذهبی علاقمند فعالیت دارید؟ ",
                               null=True, blank=True)

    sport = models.CharField(max_length=10,
                             verbose_name="در کدام زمینه ورزشی علاقمند و فعال هستید؟",
                             null=True, blank=True)

    sport_rank = models.CharField(max_length=10,
                                  verbose_name="در چه رشته ی ورزشی موفق به کسب رتبه شده اید؟",
                                  null=True, blank=True)

    academic_status = (
        (1, 'ایفای زبان انگلیسی'),
        (2, 'ریاضی'),
        (3, 'آزمایشگاه علوم تجربی'),
        (4, 'برنامه نویسی'),
    )
    academic = MultiSelectField(choices=academic_status,
                                verbose_name="در چه زمینه علمی علاقمند و فعال هستید؟",
                                null=True, blank=True)

    cultural_status = (
        (1, 'سرودن شعر'),
        (2, 'داستان نویسی'),
        (3, 'مقاله نویسی'),
        (4, 'وبلاگ نویسی'),
        (5, 'نشریه الکترونیکی'),
        (6, 'موسیقی'),
        (7, 'تولید محتوای نرم افزار'),
        (8, 'خوشنویسی'),
        (9, 'عکاسی'),
        (10, 'نقاشی'),
        (11, 'تک خوانی و آواز'),
        (12, 'کتابخوانی'),
    )
    cultural = MultiSelectField(choices=cultural_status,
                                verbose_name="در کدام زمینه فرهنگی-هنری علامند و فعال هستید؟",
                                null=True, blank=True)

    cooperation_status = (
        (1, 'سرود'),
        (2, 'نمایش و تئاتر'),
        (3, 'روزنامه دیواری'),
    )
    cooperation = MultiSelectField(choices=cooperation_status,
                                   verbose_name="علاقه به همکاری در مناسبت ها",
                                   null=True, blank=True)

    more = models.TextField(
        verbose_name="اگر تاکنون در جشنواره ها و مسابقات مختلف" +
                     " دانش آموزی عضو تیم مدرسه بوده اید و یا رتبه کسب کرده اید، لطفا یه اختصار بنویسید:",
        null=True, blank=True)

    class Meta:
        verbose_name_plural = "سابقه فعالیت های مسایقه ای دانش آموزان"
        verbose_name = "سابقه فعالیت  مسایقه ای دانش آموز"

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name}"


class StdShadModel(models.Model):
    student = models.OneToOneField('StdInfoModel', on_delete=models.CASCADE,
                                   related_name="StdShadModel",
                                   verbose_name="دانش آموز")
    smartphone_status = (
        (0, 'هیچکدام'),
        (1, 'رایانه'),
        (2, 'موبایل'),
        (3, 'تبلت'),
    )
    smartphone = models.IntegerField(choices=smartphone_status,
                                     verbose_name="دانش آموز کدام یک از این وسایل را در اختیار دارد؟",
                                     null=True)
    shad_phone = models.CharField(max_length=10, verbose_name="شماره تلفن فعال در شاد", null=True)

    class Meta:
        verbose_name_plural = "فعالیت های شاد دانش آموزان"
        verbose_name = "فعالیت شاد دانش آموز"

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name}"


class StdPlaceInfoModel(models.Model):
    student = models.OneToOneField('StdInfoModel', on_delete=models.CASCADE,
                                   related_name="StdPlaceInfoModel", verbose_name="دانش آموز")
    main_St = models.CharField(max_length=15, verbose_name="خیابان اصلی", null=True)
    auxiliary_St = models.CharField(max_length=15, verbose_name="خیابان فرعی", null=True)
    main_street = models.CharField(max_length=15, verbose_name="کوچه اصلی", null=True)
    side_alley = models.CharField(max_length=15, verbose_name="کوچه فرعی", null=True)
    plaque = models.CharField(max_length=10, verbose_name="پلاک", null=True)
    floor = models.CharField(max_length=10, verbose_name="طبقه", null=True)
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی", null=True)

    home_phone = models.CharField(max_length=10, verbose_name="تلفن منزل", blank=True, null=True)
    dad_phone = models.CharField(max_length=10, verbose_name="شماره همراه پدر", blank=True, null=True)
    mom_phone = models.CharField(max_length=10, verbose_name="شماره همراه مادر", blank=True, null=True)
    std_phone = models.CharField(max_length=10, verbose_name="شماره همراه دانش آموز", blank=True, null=True)
    dad_workplace_phone = models.CharField(max_length=10, verbose_name="تلفن محل کار پدر", blank=True, null=True)
    mom_workplace_phone = models.CharField(max_length=10, verbose_name="تلفن محل کار مادر", blank=True, null=True)
    supervisor_phone = models.CharField(max_length=10, verbose_name="تلفن همراه سرپرست دانش آموز",
                                        blank=True, null=True)
    sms_phone = models.CharField(max_length=10, verbose_name="شماره جهت دریافت پیامک های مدرسه", blank=True, null=True)

    class Meta:
        verbose_name_plural = "اطلاعات ارتباطی با دانش آموزان"
        verbose_name = "اطلاعات ارتباطی دانش آموز"

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name}"
