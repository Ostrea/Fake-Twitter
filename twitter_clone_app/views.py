from django.shortcuts import render


def home(request):
    return render(request, 'twitter_clone_app/home.html')


def help(request):
    return render(request, 'twitter_clone_app/help.html')


def about(request):
    return render(request, 'twitter_clone_app/about.html')


def contact(request):
    return render(request, 'twitter_clone_app/contact.html')


def sign_up(request):
    return render(request, 'twitter_clone_app/auth/sign_up.html')
