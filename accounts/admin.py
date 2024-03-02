from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from accounts import models

# Register your models
admin.site.site_header = 'سامانه مدیریت دانش آموزان'
admin.site.index_title = settings.SCHOOL_NAME

admin.site.register(models.StdEducationalBadModel)
admin.site.register(models.StdEducationalGoodModel)


@admin.register(models.UserModel)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("وضعیت", {'fields': ('group', 'can_edit', 'display_name')}),
    )
    list_display = ('username', 'first_name', 'last_name', 'group', 'is_staff')
    list_filter = ('group', 'is_staff')


@admin.register(models.StdGroupModel)
class StdGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'can_edit')


@admin.register(models.StdReportModel)
class CustomUserAdmin(admin.ModelAdmin):
    raw_id_fields = ('student', )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        student_id = request.GET.get('student_id')

        if student_id:
            form.base_fields['student'].initial = student_id
            form.base_fields['student'].widget.attrs['readonly'] = True
        return form


@admin.register(models.StdEducationalModel)
class StdEducationalAdmin(admin.ModelAdmin):
    raw_id_fields = ('student', )
    list_display = ('__str__', 'number', 'score')
    list_editable = ('number', 'score')
    search_fields = ('student__id_code', 'student__user__first_name', 'student__user__last_name')
    list_filter = ('negative', 'positive')

    def get_form(self, request, obj=None, **kwargs):
        _type = request.GET.get('type')
        if _type and _type == "positive":
            self.exclude = ('negative', )

        elif _type and _type == "negative":
            self.exclude = ('positive', )
        else:
            self.exclude = None

        form = super().get_form(request, obj, **kwargs)
        student_id = request.GET.get('student_id')

        if student_id:
            form.base_fields['student'].initial = student_id
            form.base_fields['student'].widget.attrs['readonly'] = True

        return form
