from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile

User = get_user_model()


class CreationForm(UserCreationForm):
    '''New user registration form.'''
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )


class EditProfileForm(forms.ModelForm):
    '''Edit profile data.'''
    class Meta():
        model = UserProfile
        fields = (
            'status',
            'birth_date',
            'avatar',
            'about',
        )
        widgets = {
            'about': forms.Textarea(
                attrs={
                    'rows': 5,
                },
            )
        }
