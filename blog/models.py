from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.conf import settings
from hitcount.models import HitCountMixin, HitCount


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recommendations = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='posts_recommendations',
                                             blank=True)
    views = GenericRelation(HitCount, object_id_field='object_pk',
                            related_query_name='views_relation')
    header_photo = models.ImageField(upload_to='posts_images/', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.post, self.content)
