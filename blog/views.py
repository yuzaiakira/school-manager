from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from core.settings import REDIRECT_FIELD_NAME
from blog.models import PostModel
from accounts.mixin import UserLoginRequiredMixin

@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def blog_view(request):
    post = PostModel.objects.all().order_by('-id')
    paginator = Paginator(post, 15)
    
    page_num = request.GET.get('page', 1)
    
    try:
        result = paginator.page(page_num)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return render(request, "blog/archive.html", {'posts': result})


@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def post_view(request, post_id):
    post = get_object_or_404(PostModel, pk=post_id)
    
    return render(request, "blog/post.html", {'post': post})


class BlogDetail(UserLoginRequiredMixin, DetailView):
    model = PostModel
    template_name = 'blog/blog-detail.html'
