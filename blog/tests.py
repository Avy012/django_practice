from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 1.1 bring post list
        response = self.client.get('/blog/')
        # 1.2 page load successfully
        self.assertEqual(response.status_code, 200)
        # 1.3 page title is 'Blog'
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # 1.4 nav bar
        navbar = soup.nav
        # 1.5 Blog, About Me is in nav bar
        self.assertIn('Blog', navbar.text)
        self.assertIn('About', navbar.text)

        # 2.1 if there is no posts in main area
        self.assertEqual(Post.objects.count(), 0)
        # 2.2 show "No Posts Yet"
        main_area = soup.find('div', id='main-area')
        self.assertIn('No Posts Yet', main_area.text)

        # 3.1 if there are 2 posts
        post_001 = Post.objects.create(
            title="first post",
            content="Hello World!!",
        )
        post_002 = Post.objects.create(
            title="second post",
            content="Bye World!!",
        )
        self.assertEqual(Post.objects.count(), 2)


        # 3.2 when you refresh the post list page
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3 main area has titles of 2 posts
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_001.title, main_area.text)
        # 3.4 "No Posts Yet" doesn't show anymore
        self.assertNotIn('No Posts Yet', main_area.text)