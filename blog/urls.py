from django.urls import path
from blog.views import blog_view, BlogDetail


app_name = "blog"

urlpatterns = [
    path('', blog_view, name='blog-list'),
    path('post/<int:pk>', BlogDetail.as_view(), name='blog-detail'),
]
