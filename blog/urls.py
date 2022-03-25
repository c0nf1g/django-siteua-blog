from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add_post/', login_required(views.AddPostView.as_view(), login_url='users:login'), name='add_post'),
    path('post/<int:post_id>', views.PostDetailView.as_view(), name='detail'),
    path('post/edit/<int:post_id>',
         login_required(views.EditPostView.as_view(), login_url='users:login'),
         name='edit_post'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount'))
]
