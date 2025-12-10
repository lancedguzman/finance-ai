from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """
    Custom registration form that includes the email field
    and enforces it as required.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class UserUpdateForm(forms.ModelForm):
    """
    Form to update the standard User model (Username/Email).
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """
    Form to update the custom Profile model (Display Name, etc.).
    """
    class Meta:
        model = Profile
        fields = ['display_name', 'email_address']
