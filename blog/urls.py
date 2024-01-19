from django.urls import path
from blog.views import blog_view, post_view


app_name = "blog"

urlpatterns = [
    path('', blog_view, name='archive'),
    path('post/<int:post_id>', post_view, name='post'),   
]
