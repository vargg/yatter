from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AboutURLTests(TestCase):
    '''Check the availability of pages and used templates
    for an unauthorized user and an authorized user.'''
    @classmethod
    def setUpClass(cls):
        '''Create test objects in db.'''
        super().setUpClass()
        cls.user = User.objects.create_user(
            'user_name',
            password='dfltusrpsswrd'
        )

    def setUp(self):
        '''Create an unauthorized client and an authorized client;
        create a list of static pages and dicts "url name: url"
        and "url name: template".'''
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(AboutURLTests.user)
        self.url_names = [
            'about',
            'tech',
        ]
        self.urls = {
            'about': reverse('about:author'),
            'tech': reverse('about:tech'),
        }
        self.templates = {
            'about': 'about/about.html',
            'tech': 'about/tech.html',
        }

    def test_urls(self):
        '''Check the HTTP status codes of the requests and used templates;
        for an unauthorized user and an authorized user.'''
        for name in self.url_names:
            with self.subTest():
                url = self.urls[name]
                template = self.templates[name]
                guest_response = self.guest_client.get(url)
                user_response = self.authorized_client.get(url)
                self.assertEqual(
                    guest_response.status_code,
                    200,
                    f'{url} does not work',
                )
                self.assertEqual(
                    user_response.status_code,
                    200,
                    f'{url} does not work',
                )
                self.assertTemplateUsed(
                    guest_response,
                    template,
                    f'{url} should use this template: {template}',
                )
                self.assertTemplateUsed(
                    user_response,
                    template,
                    f'{url} should use this template: {template}',
                )
