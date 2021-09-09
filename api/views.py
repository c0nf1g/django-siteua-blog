from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from blog.models import Post, Comment, Category
from . import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema, no_body


class PostViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = Post.objects.all()
    serializer_classes = {
        'list': serializers.RetrievePostSerializer,
        'create': serializers.CreatePostSerializer,
        'update': serializers.CreatePostSerializer
    }
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated,),
        'delete': (IsAuthenticated,)
    }

    default_serializer = serializers.RetrievePostSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()

    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=['put'])
    def recommend(self, request, pk=None):
        if pk is not None:
            try:
                post = Post.objects.get(pk=pk)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if request.data['recommendation'] == 1:
                post.recommendations.add(request.user)
                response_status = status.HTTP_200_OK
            elif request.data['recommendation'] == 0:
                post.recommendations.remove(request.user)
                response_status = status.HTTP_200_OK
            else:
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            response_status = status.HTTP_404_NOT_FOUND

        return Response(status=response_status)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_classes = {
        'create': serializers.CreateCommentSerializer,
        'list': serializers.RetrieveCommentSerializer
    }

    permission_classes_by_action = {
        'create': (IsAuthenticated,),
        'list': (AllowAny,)
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class CategoryViewSet(viewsets.ViewSet):
    serializer_class = serializers.CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        serializer = serializers.CategorySerializer(queryset, many=True)
        return Response(serializer.data)
