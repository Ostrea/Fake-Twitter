from django.urls import reverse
from django.test import TestCase

import django.contrib.auth.models as auth_models


class EditUserTests(TestCase):

    def test_edit_user_when_all_fields_are_valid(self):
        """
        Post request on `edit-user` should update user data,
        when all fields are valid and redirect to this user's profile.
        """
        old_user = auth_models.User.objects.create_user(
            'username', 'test@example.com', 'pass'
        )
        self.client.post(reverse('twitter_clone_app:log-in'),
                         {'username': 'username',
                          'email': 'test@example.com',
                          'password': 'pass',
                          'password-confirmation': 'pass'})

        response = self.client.post(reverse('twitter_clone_app:edit-user'),
                                    {'username': 'changedusername',
                                     'email': 'changed@example.com',
                                     'password': 'pass2',
                                     'password-confirmation': 'pass2'})

        self.assertEqual(len(auth_models.User.objects.all()), 1)

        new_user = auth_models.User.objects.first()

        self.assertTrue(new_user)
        self.assertEqual(new_user.id, old_user.id)
        self.assertEqual(new_user.username, 'changedusername')
        self.assertEqual(new_user.email, 'changed@example.com')

        self.assertRedirects(response, reverse('twitter_clone_app:user-profile',
                                               args=(new_user.id,)))

    def test_edit_user_shows_edit_page_when_password_does_not_match(self):
        """
        Post request on `edit-user` should show edit page with error,
        when password doesn't match password confirmation.
        """
        auth_models.User.objects.create_user(
            'username', 'test@example.com', 'pass'
        )
        self.client.post(reverse('twitter_clone_app:log-in'),
                         {'username': 'username',
                          'email': 'test@example.com',
                          'password': 'pass',
                          'password-confirmation': 'pass'})

        response = self.client.post(reverse('twitter_clone_app:edit-user'),
                                    {'username': 'username',
                                     'email': 'test@example.com',
                                     'password': 'pass',
                                     'password-confirmation': 'pass2'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/edit.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Password and password confirmation doesn\'t match.',
                      response.context['errors'])

    def test_edit_user_shows_edit_page_when_not_all_fields_are_filled(self):
        """
        Post request on `edit-user` should show edit page with error,
        when some fields are missing.
        """
        auth_models.User.objects.create_user(
            'username', 'test@example.com', 'pass'
        )
        self.client.post(reverse('twitter_clone_app:log-in'),
                         {'username': 'username',
                          'email': 'test@example.com',
                          'password': 'pass',
                          'password-confirmation': 'pass'})

        response = self.client.post(reverse('twitter_clone_app:edit-user'),
                                    {'username': '',
                                     'email': '',
                                     'password': '',
                                     'password-confirmation': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/edit.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Some fields are missing.',
                      response.context['errors'])

    def test_edit_user_shows_edit_page_with_all_errors(self):
        """
        If there are errors in submission they all should be
        shown except existing username error.
        """
        auth_models.User.objects.create_user(
            'username', 'test@example.com', 'pass'
        )
        self.client.post(reverse('twitter_clone_app:log-in'),
                         {'username': 'username',
                          'email': 'test@example.com',
                          'password': 'pass',
                          'password-confirmation': 'pass'})

        response = self.client.post(reverse('twitter_clone_app:edit-user'),
                                    {'username': '',
                                     'email': '',
                                     'password': '1',
                                     'password-confirmation': '12'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/edit.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Some fields are missing.',
                      response.context['errors'])
        self.assertIn('Password and password confirmation doesn\'t match.',
                      response.context['errors'])

    def test_change_username_to_already_existing_username(self):
        """
        Trying to change username to already existing username, should return
        `users/edit.html` with error.
        """
        auth_models.User.objects.create_user(
            'username', 'test@example.com', 'pass'
        )
        self.client.post(reverse('twitter_clone_app:log-in'),
                         {'username': 'username',
                          'email': 'test@example.com',
                          'password': 'pass',
                          'password-confirmation': 'pass'})

        auth_models.User.objects.create_user('occupiedname', 'test@test.com',
                                             'pass')

        response = self.client.post(reverse('twitter_clone_app:edit-user'),
                                    {'username': 'occupiedname',
                                     'email': 'test@example.com',
                                     'password': 'pass',
                                     'password-confirmation': 'pass'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/edit.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Username with such name already exists.',
                      response.context['errors'])
