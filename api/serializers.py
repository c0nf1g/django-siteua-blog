from rest_framework import serializers
from blog.models import Post, Comment, Category
from django.contrib.auth import get_user_model
from hitcount.models import HitCount


class BlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'profile_photo')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class HitObjectRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        if isinstance(value, HitCount):
            return 'Post: ' + str(value.hits)

        raise Exception('Unexpected type of tagged object')


class RetrievePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = BlogUserSerializer()
    recommendations = serializers.SlugRelatedField(slug_field='email', read_only=True, many=True)
    views = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'category',
                  'content', 'published', 'author',
                  'recommendations', 'header_photo', 'views')

    def get_views(self, obj):
        return obj.hit_count.hits


class CreatePostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('id', 'title', 'category',
                  'content', 'author', 'header_photo')


class RetrieveCommentSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(slug_field='id', read_only=True)
    author = BlogUserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author',
                  'post', 'published')


class CreateCommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author',
                  'post')
