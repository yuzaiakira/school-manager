from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from blog.models import PostModel
from accounts.mixin import UserLoginRequiredMixin


class BlogDetail(UserLoginRequiredMixin, DetailView):
    model = PostModel
    template_name = 'blog/blog-detail.html'


class BlogList(UserLoginRequiredMixin, ListView):
    model = PostModel
    context_object_name = 'blog'
    template_name = 'blog/blog-list.html'
    paginate_by = 1
