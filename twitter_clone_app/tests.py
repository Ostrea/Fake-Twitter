from django.urls import reverse
from django.test import TestCase


class ViewTests(TestCase):

    def test_index_view(self):
        """
        Should get 'index.html' template.
        """
        response = self.client.get(reverse('twitter_clone_app:index'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                         "twitter_clone_app/index.html")

    def test_help_view(self):
        """
        Should get 'help.html' template.
        """
        response = self.client.get(reverse('twitter_clone_app:help'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                         "twitter_clone_app/help.html")
