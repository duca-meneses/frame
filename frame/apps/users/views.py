from django.shortcuts import redirect, render

from .forms import ProfileForm


def profile_view(request):
    profile = request.user.profile
    return render(request, 'apps/users/profile.html', {'profile': profile})


def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'apps/users/profile_edit.html', {'form': form})
