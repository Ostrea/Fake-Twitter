from django.urls import reverse
from django.test import TestCase
import django.contrib.auth.models as auth_models


class ViewTests(TestCase):

    def test_home_view(self):
        """
        Should get 'home.html' template with appropriate title.
        """
        response = self.client.get(reverse('twitter_clone_app:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'twitter_clone_app/home.html')
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
        Should get 'about.html' template with appropriate title.
        """
        response = self.client.get(reverse('twitter_clone_app:about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'twitter_clone_app/about.html')
        self.assertContains(response, '<title>About | Fake Twitter</title>',
                            html=True)

    def test_contact_view(self):
        """
        Should get 'contact.html' template with appropriate title.
        """
        response = self.client.get(reverse('twitter_clone_app:contact'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'twitter_clone_app/contact.html')
        self.assertContains(response, '<title>Contact | Fake Twitter</title>',
                            html=True)


class AuthViewTests(TestCase):

    def test_sign_up_view(self):
        """
        Should get 'auth/new_user.html' template with appropriate title.
        """
        response = self.client.get(reverse('twitter_clone_app:sign-up'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/sign_up.html')
        self.assertContains(response, '<title>Sign up | Fake Twitter</title>',
                            html=True)


class UserViewTests(TestCase):

    def test_profile_page_view_with_existing_user(self):
        """
        Should get 'user_detail.html' template with appropriate title
        when user exists.
        """
        existing_user = auth_models.User.objects.create_user(
            'Test user name', 'test email', '123456')

        response = self.client.get(reverse('twitter_clone_app:user-profile',
                                           args=(existing_user.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/profile.html')
        self.assertContains(response, '<title>Profile | Fake Twitter</title>',
                            html=True)

    def test_profile_page_view_with_non_existing_user(self):
        """
        Should return 404.
        """
        response = self.client.get(reverse('twitter_clone_app:user-profile',
                                           args=(1,)))

        self.assertEqual(response.status_code, 404)
