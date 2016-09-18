from django.urls import reverse
from django.test import TestCase

import django.contrib.auth.models as auth_models
import unittest.mock as mock


class LogInLogOutTests(TestCase):

    def test_log_in_post_should_redirect_to_profile_when_valid_credentials(
            self):
        """
        Should redirect to logined user profile page,
        when username and password are valid.
        """
        user = auth_models.User.objects.create_user('username', 'test@test.com',
                                                    'pass')

        response = self.client.post(reverse('twitter_clone_app:log-in'),
                                    {'username': 'username',
                                     'password': 'pass'})

        self.assertRedirects(response, reverse('twitter_clone_app:user-profile',
                                               args=(user.id,)))

    def test_log_in_post_should_show_login_page_when_invalid_credentials(self):
        """
        Should show login page with error when username or password are invalid.
        """
        auth_models.User.objects.create_user('username', 'test@test.com',
                                             'pass')

        response = self.client.post(reverse('twitter_clone_app:log-in'),
                                    {'username': 'usernam',
                                     'password': 'pas'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/log_in.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Wrong credentials.', response.context['errors'])

    @mock.patch('twitter_clone_app.views.logout', autospec=True)
    def test_log_out(self, django_auth_logout_mock):
        """
        Post to log out url should call django logout and redirect to home.
        """
        response = self.client.post(reverse('twitter_clone_app:log-out'))

        self.assertRedirects(response, reverse('twitter_clone_app:home'))
        django_auth_logout_mock.assert_called_once_with(mock.ANY)
