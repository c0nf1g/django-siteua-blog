from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description"
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('comments', views.CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/doc', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include(router.urls))
]
