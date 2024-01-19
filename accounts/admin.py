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
    list_display = ['username', 'first_name', 'last_name', 'group', 'is_staff']
    list_filter = ['group', 'is_staff']


@admin.register(models.StdGroupModel)
class StdGroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'can_edit']

