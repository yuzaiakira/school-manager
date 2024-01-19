from django.contrib import admin
from information import models



@admin.register(models.StdInfoModel)
class StdInfoAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'id_code', 'get_group')
    list_filter = ('user__group', )
    search_fields = ('id_code', 'user__first_name', 'user__last_name')

    @admin.display(ordering='user__first_name', description='نام')
    def get_first_name(self, obj):
        return obj.user.first_name

    @admin.display(ordering='user__last_name', description='نام خانوادگی')
    def get_last_name(self, obj):
        return obj.user.last_name

    @admin.display(ordering='user__group', description='گروه')
    def get_group(self, obj):
        return obj.user.group


@admin.register(models.FatherInfoModel)
class FatherInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'id_code', 'student', 'get_group')
    list_filter = ('student__user__group',)
    search_fields = ('id_code', 'first_name', 'last_name', 'student__user__first_name', 'student__user__last_name')

    @admin.display(ordering='user__group', description='گروه')
    def get_group(self, obj):
        return obj.student.user.group


@admin.register(models.MatherInfoModel)
class MatherInfoAdmin(FatherInfoAdmin):
    pass


@admin.register(models.SupervisorInfoModel)
class SupervisorInfoAdmin(FatherInfoAdmin):
    pass


@admin.register(models.StdLastSchoolModel)
class StdLastSchoolAdmin(FatherInfoAdmin):
    list_display = ('student', 'get_group')
    list_filter = ('student__user__group',)
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__id_code')


@admin.register(models.StdCompetitionsModel)
class StdCompetitionsAdmin(StdLastSchoolAdmin):
    pass


@admin.register(models.StdShadModel)
class StdShadAdmin(StdLastSchoolAdmin):
    pass


@admin.register(models.StdPlaceInfoModel)
class StdPlaceInfoAdmin(StdLastSchoolAdmin):
    pass
