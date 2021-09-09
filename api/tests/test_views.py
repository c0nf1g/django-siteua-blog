import json
from rest_framework.test import APIClient, APITestCase
from blog.models import Post, Category, Comment
from api.serializers import RetrievePostSerializer, RetrieveCommentSerializer, CategorySerializer
from rest_framework import status
from rest_framework.reverse import reverse
from api.tests import helpers
from tests import SetupTestData


class PostViewSetTest(SetupTestData):
    client_class = APIClient

    def setUp(self):
        super().setUp()
        self.posts = helpers.create_posts(self.user)

        self.valid_post_payload = {
            'title': 'test_title',
            'category': self.posts[0].category.id,
            'content': 'test_content'
        }

        self.invalid_post_payload = {
            'title': '',
            'content': '',
            'category': 1
        }

        self.add_recommendation_payload = {
            'recommendation': 1
        }

        self.delete_recommendation_payload = {
            'recommendation': 0
        }

        self.invalid_recommendation_payload = {
            'recommendation': -1
        }

    def test_get_all_posts(self):
        response = self.client.get(reverse('api:posts-list'))
        posts = Post.objects.all()
        serializer = RetrievePostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_get_single_post(self):
        response = self.client.get(reverse('api:posts-detail', kwargs={'pk': self.posts[0].id}))
        post = Post.objects.get(pk=self.posts[0].id)
        serializer = RetrievePostSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_get_single_post(self):
        response = self.client.get(reverse('api:posts-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_create_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(path=reverse('api:posts-list'),
                                    data=json.dumps(self.valid_post_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(path=reverse('api:posts-list'),
                                    data=json.dumps(self.invalid_post_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(path=reverse('api:posts-detail', kwargs={'pk': self.posts[0].id}),
                                   data=json.dumps(self.valid_post_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(path=reverse('api:posts-detail', kwargs={'pk': self.posts[0].id}),
                                   data=json.dumps(self.invalid_post_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(reverse('api:posts-detail', kwargs={'pk': self.posts[0].id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(reverse('api:posts-detail', kwargs={'pk': 31}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_add_post_recommendation(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(path=reverse('api:posts-recommend', kwargs={'pk': self.posts[0].id}),
                                   data=json.dumps(self.add_recommendation_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_remove_post_recommendation(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(path=reverse('api:posts-recommend', kwargs={'pk': self.posts[0].id}),
                                   data=json.dumps(self.delete_recommendation_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_post_recommendation(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(path=reverse('api:posts-recommend', kwargs={'pk': self.posts[0].id}),
                                   data=json.dumps(self.invalid_recommendation_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_add_post_recommendation(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(path=reverse('api:posts-recommend', kwargs={'pk': 32}),
                                   data=json.dumps(self.add_recommendation_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentViewSet(SetupTestData):
    client_class = APIClient

    def setUp(self):
        super().setUp()
        self.comments = helpers.create_comments(self.user)

        self.valid_comment_payload = {
            'content': 'my test content',
            'post': self.comments[0].post.id
        }

        self.invalid_comment_payload = {
            'content': '',
            'post': 23
        }

    def test_get_all_comments(self):
        response = self.client.get(reverse('api:comments-list'))
        comments = Comment.objects.all()
        serializer = RetrieveCommentSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_create_comment(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(path=reverse('api:comments-list'),
                                    data=json.dumps(self.valid_comment_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_comment(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(path=reverse('api:comments-list'),
                                    data=json.dumps(self.invalid_comment_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CategoryViewSetTest(APITestCase):
    def setUp(self):
        helpers.create_categories()

    def test_get_all_categories(self):
        response = self.client.get(reverse('api:categories-list'))
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
