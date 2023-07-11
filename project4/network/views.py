from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post


@login_required
def index(request):
    context = {
        ''
    }
    return render(request, "network/index.html")


@login_required
def user_page_view(request, user_slug):
    try:
        curr_user = User.objects.get(slug=user_slug)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == 'POST':
        if 'post_content' in request.POST and request.POST['post_content']:
            post_content = request.POST['post_content']
            new_post = Post.objects.create(
                author=request.user,
                content=post_content,
            )
        return redirect('user_page_view', user_slug)

    #pagination
    user_posts = Post.objects.filter(author=curr_user).order_by('-id')
    pagination_range = 10
    paginator = Paginator(user_posts, pagination_range)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    context = {
        'curr_user': curr_user,
        'user_posts': user_posts,
        'page_obj': page_object,
        'user_followers': 0,
        'user_self_follows': 0,
    }
    return render(request, 'network/user_page.html', context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
