from django.shortcuts import render
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


class UserProfileView(generic.DetailView):
    model = auth_models.User
    template_name = 'twitter_clone_app/users/profile.html'
