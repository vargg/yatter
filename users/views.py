from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

from .forms import CreationForm, EditProfileForm
from .models import UserProfile

User = get_user_model()


class SignUp(CreateView):
    '''Login page.'''
    form_class = CreationForm
    template_name = 'users/signup.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(
            username=username,
            password=password,
        )
        login(self.request, user)  # instant authentication
        return redirect('posts:index')


@login_required
def edit_profile(request, username):
    '''Edit additional user profile information.'''
    profile_user = get_object_or_404(
        User,
        username=username,
    )
    if request.user != profile_user:
        return redirect(
            'posts:profile',
            username=username,
        )
    profile = UserProfile.objects.get_or_create(user=profile_user)[0]
    form = EditProfileForm(
        instance=profile,
    )
    if request.method == 'POST':
        form = EditProfileForm(
            request.POST or None,
            files=request.FILES or None,
            instance=profile,
        )
        if form.is_valid():
            form.save()
            return redirect(
                'posts:profile',
                username=username,
            )
    return render(
            request,
            'users/edit_profile.html',
            {
                'form': form,
            }
        )
