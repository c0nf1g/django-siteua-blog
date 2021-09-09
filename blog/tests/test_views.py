from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from blog.tests import helpers
from tests import SetupTestData


class HomeTemplateViewTest(TestCase):
    def test_get_homepage(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AddPostTemplateViewTest(SetupTestData):
    def test_get_add_post_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:add_post'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SetupPostViewTestData(SetupTestData):
    def setUp(self):
        super().setUp()
        self.politics_category = helpers.create_politics_category()
        self.post = helpers.create_post(self.user, self.politics_category)


class PostDetailViewTest(SetupPostViewTestData):
    def setUp(self):
        super().setUp()

    def test_get_post_detail_page(self):
        response = self.client.get(reverse('blog:detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        self.assertContains(response, self.post.category)
        self.assertContains(response, self.post.author.first_name)
        self.assertContains(response, self.post.author.last_name)
        self.assertContains(response, self.post.header_photo)


class EditPostDetailViewTest(SetupPostViewTestData):
    def setUp(self):
        super().setUp()

    def test_get_edit_post_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:edit_post', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        self.assertContains(response, self.post.header_photo)
