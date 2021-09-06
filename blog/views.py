from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import BlogPost, BlogComment

# Create your views here.


def blog(request):
    """
    Displays all blog posts.
    """

    blogposts = BlogPost.objects.all().order_by("-date")

    context = {
        'blogposts': blogposts,
    }

    return render(request, 'blog/blog.html', context)


def blog_detail(request, blogpost_id):
    """
    Display blog detail page.
    """

    blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
    comments = BlogComment.objects.filter(blogpost=blogpost)

    context = {
        'blogpost': blogpost,
        'comments': comments,
    }

    return render(request, 'blog/blog_detail.html', context)
