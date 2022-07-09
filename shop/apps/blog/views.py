from django.views.generic import ListView, DetailView
from .models import Blog


class BlogListView(ListView):
    queryset = Blog.objects.filter(status=1).order_by('-created_on')
    model = Blog
    template_name = 'blog/index.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/post_details.html'