from django.urls import reverse
from django.test import TestCase

import django.contrib.auth.models as auth_models
import unittest.mock as mock


class CreateUserTests(TestCase):

    @mock.patch('twitter_clone_app.views.login', autospec=True)
    def test_create_user_when_all_fields_are_valid(self,
                                                   django_auth_login_mock):
        """
        Post request on `create-user` should create new user,
        when all fields are valid and redirect to this user's profile.
        """
        response = self.client.post(reverse('twitter_clone_app:create-user'),
                                    {'username': 'test user',
                                     'email': 'test email',
                                     'password': 'pass',
                                     'password-confirmation': 'pass'})

        new_user = auth_models.User.objects.first()

        self.assertTrue(new_user)
        self.assertEqual(new_user.username, 'test user')
        self.assertEqual(new_user.email, 'test email')

        self.assertRedirects(response, reverse('twitter_clone_app:user-profile',
                                               args=(new_user.id,)))

        django_auth_login_mock.assert_called_once_with(mock.ANY, new_user)

    def test_create_user_shows_sign_up_when_not_all_fields_are_filled(self):
        """
        Post request on `create-user` should show sign up once again,
        when some fields are missing.
        """
        response = self.client.post(reverse('twitter_clone_app:create-user'),
                                    {'username': '',
                                     'email': '',
                                     'password': '',
                                     'password-confirmation': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/signup.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Some fields are missing.',
                      response.context['errors'])

    def test_create_user_shows_sign_up_when_password_does_not_match(self):
        """
        Post request on `create-user` should show sign up once again,
        when password doesn't match password confirmation.
        """
        response = self.client.post(reverse('twitter_clone_app:create-user'),
                                    {'username': 'test user',
                                     'email': 'test email',
                                     'password': 'pass',
                                     'password-confirmation': 'pass2'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/signup.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Password and password confirmation doesn\'t match.',
                      response.context['errors'])

    def test_create_user_shows_sign_up_with_all_errors(self):
        """
        If there are errors in submission they all should be
        shown except existing username error.
        """
        response = self.client.post(reverse('twitter_clone_app:create-user'),
                                    {'username': '',
                                     'email': '',
                                     'password': '1',
                                     'password-confirmation': '12'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/signup.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Some fields are missing.',
                      response.context['errors'])
        self.assertIn('Password and password confirmation doesn\'t match.',
                      response.context['errors'])

    def test_sign_up_with_existing_username(self):
        """
        Trying to sign up with already existing username, should return
        `users/signup.html` with error.
        """
        auth_models.User.objects.create_user('username', 'test@test.com',
                                             'pass')

        response = self.client.post(reverse('twitter_clone_app:create-user'),
                                    {'username': 'username',
                                     'email': 'email',
                                     'password': '12',
                                     'password-confirmation': '12'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/signup.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Username with such name already exists.',
                      response.context['errors'])
