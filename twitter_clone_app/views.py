from django.shortcuts import render, get_object_or_404
from django.views import generic
import django.contrib.auth.models as auth_models


def home(request):
    return render(request, 'twitter_clone_app/home.html')


def help(request):
    return render(request, 'twitter_clone_app/help.html')


def about(request):
    return render(request, 'twitter_clone_app/about.html')


def contact(request):
    return render(request, 'twitter_clone_app/contact.html')


def sign_up(request):
    return render(request, 'twitter_clone_app/users/sign_up.html')


def user_profile(request, user_id):

    def gravatar_for(user_email):
        import hashlib

        gravatar_id = (hashlib.md5(user_email.lower().encode('utf-8'))
                       .hexdigest())
        return 'https://secure.gravatar.com/avatar/' + gravatar_id

    user = get_object_or_404(auth_models.User, pk=user_id)
    return render(request, 'twitter_clone_app/users/profile.html',
                  {'user': user, 'gravatar_url': gravatar_for(user.email)})
