from .models import Post
from django.views import generic
from hitcount import views


class HomeView(generic.TemplateView):
    template_name = 'blog/home.html'


class AddPostView(generic.TemplateView):
    template_name = 'blog/addPost.html'


class PostDetailView(views.HitCountDetailView):
    model = Post
    template_name = 'blog/postDetail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    count_hit = True


class EditPostView(generic.DetailView):
    model = Post
    template_name = 'blog/editPost.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
