from apps.posts.forms import ReplyCreateForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProfileForm


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()

    posts = profile.user.posts.all()

    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(
                num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(
                num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            replyform = ReplyCreateForm()
            template = 'snippets/loop_profile_comments.html'
            context = {'comments': comments, 'replyform': replyform}
            return render(request, template, context)
        elif 'liked-posts' in request.GET:
            posts = profile.user.likedposts.order_by('-likedpost__created_at')
        template = 'snippets/loop_profile_posts.html'
        return render(request, template, {'posts': posts})

    context = {
        'profile': profile,
        'posts': posts
    }

    return render(request, 'apps/users/profile.html', context)


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            return redirect('profile')

    if request.path == reverse('profile-onboarding'):
        template = 'apps/users/profile_onboarding.html'
    else:
        template = 'apps/users/profile_edit.html'

    return render(request, template, {'form': form})


@login_required
def profile_delete_view(request):
    user = request.user

    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Conta deletada com sucesso')
        return redirect('home')
    return render(request, 'apps/users/profile_delete.html')
