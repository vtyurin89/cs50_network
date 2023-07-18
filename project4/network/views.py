import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post, Follow


@login_required
def index(request):
    all_posts = Post.objects.all().order_by('-id')

    # pagination
    pagination_range = 10
    paginator = Paginator(all_posts, pagination_range)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    context = {
        'page_object': page_object,
    }
    return render(request, "network/index.html", context)


@login_required
def following_posts(request):
    following_posts = Post.objects.filter(author__in=User.objects.filter(is_followed_by__follower=request.user)).order_by('-id')

    # pagination
    pagination_range = 10
    paginator = Paginator(following_posts, pagination_range)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    context = {
        'page_object': page_object,
    }
    return render(request, "network/following.html", context)


@login_required
def edit_post(request, post_id):
    try:
        my_post = Post.objects.get(id=post_id, author=request.user)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found!'}, status=404)
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('content') is not None:
            my_post.content = data['content']
        my_post.save()
        return HttpResponse(status=204)
    elif request.method == "GET":
        return JsonResponse(my_post.serialize())

        # Only PUT or GET request!
    else:
        return JsonResponse({
        "error": "PUT or GET request required."
        }, status=400)


@login_required
def like_post(request, post_id):
    try:
        my_post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found!'}, status=404)
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('set_like') is not None:
            if request.user in my_post.liked.all():
                my_post.liked.remove(request.user)
                like_now = False
            else:
                my_post.liked.add(request.user)
                like_now = True
            my_post.save()
            return JsonResponse({
                "set_like": 'like_now',
            }, status=204)
    # Only PUT request!
    else:
        return JsonResponse({
            "error": "PUT or GET request required."
        }, status=400)



@login_required
def user_page_view(request, user_slug):
    try:
        curr_user = User.objects.get(slug=user_slug)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'POST':

        #write a post
        if 'post_content' in request.POST and request.POST['post_content']:
            post_content = request.POST['post_content']
            new_post = Post.objects.create(
                author=request.user,
                content=post_content,
            )

        #follow/unfollow
        elif 'follow' in request.POST:
            change_follow = Follow.objects.create(
                user=curr_user,
                follower=request.user,
            )
            change_follow.save()
        elif 'unfollow' in request.POST:
            change_unfollow = Follow.objects.get(
                user=curr_user,
                follower=request.user,
            )
            change_unfollow.delete()
        return redirect('user_page_view', user_slug)

    #pagination
    user_posts = Post.objects.filter(author=curr_user).order_by('-id')
    pagination_range = 10
    paginator = Paginator(user_posts, pagination_range)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    #info
    user_followers = Follow.objects.filter(user=curr_user)
    user_self_follows = Follow.objects.filter(follower=curr_user)
    try:
        check_follow = user_followers.get(follower=request.user)
    except ObjectDoesNotExist:
        check_follow = False

    context = {
        'curr_user': curr_user,
        'page_object': page_object,
        'user_followers': len(user_followers),
        'user_self_follows': len(user_self_follows),
        'check_follow': check_follow,
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

