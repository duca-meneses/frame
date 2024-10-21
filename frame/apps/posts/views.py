import httpx
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import PostCreateForm, PostEditForm
from .models import Post, Tag


def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()

    categories = Tag.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'tag': tag
    }

    return render(request, 'apps/posts/home.html', context)


@login_required
def post_create_view(request):
    form = PostCreateForm()

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = httpx.get((form.data['url']))
            source_code = BeautifulSoup(website.text, 'html.parser')

            find_image = source_code.select('meta[content^="https://live.staticflickr.com/"]')
            image = find_image[0]['content']
            post.image = image

            find_title = source_code.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title

            find_artist = source_code.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist

            post.author = request.user

            post.save()
            form.save_m2m()
            return redirect('home')

    return render(request, 'apps/posts/post_create.html', {'form': form})


@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Postagem deletada com sucesso')
        return redirect('home')

    return render(request, 'apps/posts/post_delete.html', {'post': post})


@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    form = PostEditForm(instance=post)

    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Postagem atualizada com sucesso')
            return redirect('home')

    context = {
        'post': post,
        'form': form
    }

    return render(request, 'apps/posts/post_edit.html', context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'apps/posts/post_page.html', {'post': post})
