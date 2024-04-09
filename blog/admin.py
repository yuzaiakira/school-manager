from django.contrib import admin
from .models import PostModel
from blog.forms import PostForm


class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('title', 'author', 'updated_on', 'created_on')
    list_filter = ('updated_on', 'created_on')
    search_fields = ('title', 'author',)
    ordering = ('-updated_on', '-id')
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


admin.site.register(PostModel, PostAdmin)
