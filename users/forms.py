from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from .models import BlogUser


class BlogUserCreationForm(UserCreationForm):
    class Meta:
        model = BlogUser
        fields = ('email', 'first_name', 'last_name')


class BlogUserChangeForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_photo = forms.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = BlogUser
        fields = ('email', 'first_name', 'last_name', 'profile_photo')


class BlogUserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = BlogUser
        fields = ('old_password', 'new_password1', 'new_password2')
