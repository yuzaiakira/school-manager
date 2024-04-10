from django.urls import path
from blog.views import BlogList, BlogDetail


app_name = "blog"

urlpatterns = [
    path('', BlogList.as_view(), name='blog-list'),
    path('post/<int:pk>', BlogDetail.as_view(), name='blog-detail'),
]
