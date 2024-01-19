from django.contrib import admin
from .models import PostModel
from django_summernote.admin import SummernoteModelAdmin



class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    
    list_display = ('title', 'author')
    fieldsets = [
        (None, { 'fields': [('title','content','pic')] } ),
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()
            
admin.site.register(PostModel, PostAdmin)

