# blog/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Blog


class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.post = Blog.objects.create(
            title='A good title',
            body='Nice body content',
        )

    def test_string_representation(self):
        post = Blog(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.body}', 'Nice body content')

    def test_post_list_view(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'content')
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_post_detail_view(self):
        response = self.client.get('/a-good-title/')
        no_response = self.client.get('/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'posts/post_details.html')