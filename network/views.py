import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Profile, Post

def index(request):
    return render(request, "network/index.html")

@csrf_exempt
@login_required
def create_post(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    # Check post text
    text = data.get("text", "")
    if text == "":
        return JsonResponse({
            "error": "Text cannot be empty"
        }, status=400)
    
    post = Post(
        user=request.user,
        body=text,
    )
    post.save()
    
    return JsonResponse({"message": "Email sent successfully."}, status=201)

@login_required
def modify_post(request):
    pass

@csrf_exempt
@login_required
def profile(request, user_pk):

    try:
        profile = Profile.objects.get(user=user_pk)
        
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(profile.serialize(request.user.pk))
    elif request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        user_profile = Profile.objects.get(user=request.user.pk)
        other_user = User.objects.get(pk=user_pk)
        if data.get("follow") is not None:
            print("follow")
            user_profile.following.add(other_user)
            profile.followers.add(request.user)
        elif data.get("unfollow") is not None:
            print("unfollow")
            user_profile.following.remove(other_user)
            profile.followers.remove(request.user)
        else:
            print(False)
        
        profile.save()
        user_profile.save()
        
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT request required"
        }, status=400)

def get_posts(request, post_type, get_page_no=1):

    print(post_type)
    print(get_page_no)
    
    try:
        all_posts = Post.objects.order_by("-timestamp").all()
        if post_type == "All Posts":
            pass
        elif post_type == "Posts by Following":
            profile = Profile.objects.get(user=request.user)
            all_posts = all_posts.filter(user__in=profile.following.all())
        elif "User" in post_type:
            ## Example: "User 1"
            print(post_type)
            user_pk = [int(s) for s in post_type.split() if s.isdigit()][0]
            print(user_pk)
            user = User.objects.get(pk=user_pk)
            all_posts = all_posts.filter(user=user)            
            
        p = Paginator(all_posts, 10)
    except:
        return JsonResponse({"error": "Error occured when requesting posts"}, status=404)
    
    page = p.page(get_page_no)
    posts = [post.serialize(request.user.pk) for post in page.object_list]
    return JsonResponse({
        "page_number": page.number,
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
        "posts": posts
    }, safe=False)

@csrf_exempt
@login_required
def post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Update post
    if request.method == "GET":
        return JsonResponse(post.serialize(request.user.pk))
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is not None:
            post.likes.add(request.user)
        elif data.get("unlike") is not None:
            post.likes.remove(request.user)
        elif data.get("edit_body") is not None:
            # Ensure post is made by user
            if post.user != request.user:
                return JsonResponse({"error": "Current user must match post's creator"}, status=404)
            post.body = data["edit_body"]
            
            post.save()
            return JsonResponse(post.serialize(request.user.pk))
        
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

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
            profile = Profile(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
