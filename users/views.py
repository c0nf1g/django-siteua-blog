from django.shortcuts import get_object_or_404
from .forms import BlogUserCreationForm, BlogUserChangeForm, BlogUserChangePasswordForm
from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


class ProfileView(generic.DetailView):
    model = get_user_model()
    template_name = 'users/userProfile.html'
    pk_url_kwarg = 'user_id'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = get_object_or_404(get_user_model(), id=self.kwargs['user_id'])
        context['blog_user'] = user
        return context


class RegisterView(generic.CreateView):
    form_class = BlogUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'users/logout.html'


class EditView(generic.UpdateView):
    form_class = BlogUserChangeForm
    template_name = 'users/editProfile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'user_id': self.request.user.id})


class ChangeBlogUserPassword(auth_views.PasswordChangeView):
    form_class = BlogUserChangePasswordForm
    template_name = 'users/changePassword.html'
    success_url = reverse_lazy('blog:home')
