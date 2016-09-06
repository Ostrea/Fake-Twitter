from django.urls import reverse
from django.test import TestCase


class ViewTests(TestCase):

    def test_index_view(self):
        """
        Should get 'index.html' template with appropriate title.
        """
        response = self.client.get(reverse('twitter_clone_app:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'twitter_clone_app/index.html')
        self.assertContains(response, '<title>Home | Fake Twitter</title>',
                            html=True)

    def test_help_view(self):
        """
        Should get 'help.html' template with appropriate title.
        """
        response = self.client.get(reverse('twitter_clone_app:help'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'twitter_clone_app/help.html')
        self.assertContains(response, '<title>Help | Fake Twitter</title>',
                            html=True)

    def test_about_view(self):
        """
        Should get 'about.html' template.
        """
        response = self.client.get(reverse('twitter_clone_app:about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'twitter_clone_app/about.html')
