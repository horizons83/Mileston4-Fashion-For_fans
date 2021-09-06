from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BlogPost, BlogComment
from .forms import BlogForm, CommentForm

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


@login_required
def add_blogpost(request):
    """
    Create Add blog post form for admin only.
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost = form.save()
            messages.success(request, 'Successfully added blog post!')
            return redirect(reverse('blog_detail', args=[blogpost.id]))
        else:
            messages.error(
                        request,
                        'Failed to add blog post.\
                        Please ensure the form is valid.')
    else:
        form = BlogForm()
        template = 'blog/add_blogpost.html'
        context = {
            'form': form,
        }

    return render(request, template, context)
