from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    return render(request, 'twitter_clone_app/users/signup.html')


@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == 'GET':
        return render(request, 'twitter_clone_app/users/login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return HttpResponseRedirect(reverse('twitter_clone_app:user-profile',
                                    args=(user.id,)))
    else:
        return render(request, 'twitter_clone_app/users/login.html', {
            'errors': ['Wrong credentials.']
        })


@require_POST
def create_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password_confirmation = request.POST['password-confirmation']

    errors = []
    if (not username or not email or
            not password or not password_confirmation):
        errors.append('Some fields are missing.')
    if password != password_confirmation:
        errors.append('Password and password confirmation doesn\'t match.')
    if errors:
        return render(request, 'twitter_clone_app/users/signup.html', {
            'errors': errors
        })

    try:
        new_user = auth_models.User.objects.create_user(
            username, email, password
        )
    except IntegrityError:
        return render(request, 'twitter_clone_app/users/signup.html', {
            'errors': ['Username with such name already exists.']
        })

    login(request, new_user)

    return HttpResponseRedirect(reverse('twitter_clone_app:user-profile',
                                        args=(new_user.id,)))


def gravatar_for(user_email):
    import hashlib

    gravatar_id = (hashlib.md5(user_email.lower().encode('utf-8'))
                   .hexdigest())
    return 'https://secure.gravatar.com/avatar/' + gravatar_id


def user_profile(request, user_id):
    user = get_object_or_404(auth_models.User, pk=user_id)
    return render(request, 'twitter_clone_app/users/profile.html',
                  {'user': user, 'gravatar_url': gravatar_for(user.email)})


@require_POST
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('twitter_clone_app:home'))


@require_http_methods(['GET', 'POST'])
@login_required(login_url='/login/', redirect_field_name='')
def edit_user(request):
    if request.method == 'GET':
        return render(request, 'twitter_clone_app/users/edit.html',
                      {'gravatar_url': gravatar_for(request.user.email)})

    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password_confirmation = request.POST['password-confirmation']

    errors = []
    if (not username or not email or
            not password or not password_confirmation):
        errors.append('Some fields are missing.')
    if password != password_confirmation:
        errors.append('Password and password confirmation doesn\'t match.')
    if errors:
        return render(request, 'twitter_clone_app/users/edit.html', {
            'errors': errors
        })

    request.user.username = username
    request.user.email = email
    request.user.set_password(password)

    try:
        request.user.save()
    except IntegrityError:
        return render(request, 'twitter_clone_app/users/edit.html', {
            'errors': ['Username with such name already exists.']
        })

    update_session_auth_hash(request, request.user)

    return HttpResponseRedirect(reverse('twitter_clone_app:user-profile',
                                        args=(request.user.id,)))


@login_required(login_url='/login/', redirect_field_name='')
def show_all_users(request):
    users = auth_models.User.objects.all()
    paginator = Paginator(users, 25)

    page = request.GET.get('page')
    try:
        paginated_users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_users = paginator.page(paginator.num_pages)

    users_with_gravatar = {user: gravatar_for(user.email)
                           for user in paginated_users}

    return render(request, 'twitter_clone_app/users/all.html',
                  {'users': users, 'users_with_gravatar': users_with_gravatar,
                   'page': paginated_users})
