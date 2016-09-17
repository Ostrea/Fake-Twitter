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


class AuthTests(TestCase):

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

    def test_create_user_creates_user_when_all_fields_are_valid(self):
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

        self.assertRedirects(response, reverse('twitter_clone_app:user-profile',
                                               args=(new_user.id,)))

        self.assertTrue(new_user)
        self.assertEqual(new_user.username, 'test user')
        self.assertEqual(new_user.email, 'test email')

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
                                'twitter_clone_app/users/sign_up.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Password and password confirmation doesn\'t match.',
                      response.context['errors'])

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
                                'twitter_clone_app/users/sign_up.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Some fields are missing.',
                      response.context['errors'])

    def test_create_user_shows_sign_up_with_all_errors(self):
        """
        If there are errors in submission they all should be
        shown.
        """
        response = self.client.post(reverse('twitter_clone_app:create-user'),
                                    {'username': '',
                                     'email': '',
                                     'password': '1',
                                     'password-confirmation': '12'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/sign_up.html')

        self.assertTrue(response.context['errors'])
        self.assertIn('Some fields are missing.',
                      response.context['errors'])
        self.assertIn('Password and password confirmation doesn\'t match.',
                      response.context['errors'])

    def test_login_view(self):
        """
        Should get 'auth/login.html' template with appropriate title.
        """
        response = self.client.get(reverse('twitter_clone_app:log-in'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'twitter_clone_app/users/log_in.html')
        self.assertContains(response, '<title>Log in | Fake Twitter</title>',
                            html=True)

    def test_login_post_should_redirect_to_profile_when_valid_credentials(self):
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

    def test_login_post_should_show_login_page_when_invalid_credentials(self):
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
