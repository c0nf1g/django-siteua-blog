from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditView.as_view(), name='edit_profile'),
    path('profile/password/', views.ChangeBlogUserPassword.as_view(), name='password')
]
