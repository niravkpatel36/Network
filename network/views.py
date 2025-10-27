import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import User, Post, Like, Follow

# -------------------------
# Auth views (simple)
# -------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("network:index")
        return render(request, "network/login.html", {"message": "Invalid credentials."})
    return render(request, "network/login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("network:index")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if password != confirmation:
            return render(request, "network/register.html", {"message": "Passwords must match."})
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except Exception as e:
            return render(request, "network/register.html", {"message": f"Could not register: {e}"})
        login(request, user)
        return redirect("network:index")
    return render(request, "network/register.html")

# -------------------------
# Pages & API
# -------------------------
def index(request):
    posts_qs = Post.objects.select_related("user").all()
    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    user_likes = set()
    if request.user.is_authenticated:
        user_likes = set(request.user.likes.values_list("post_id", flat=True))

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "user_likes": user_likes,
    })

@login_required
@require_http_methods(["POST"])
def create_post(request):
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    content = data.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "Content cannot be empty."}, status=400)
    if len(content) > 1000:
        return JsonResponse({"error": "Content too long."}, status=400)
    post = Post.objects.create(user=request.user, content=content, timestamp=timezone.now())
    return JsonResponse({
        "message": "created",
        "post": {
            "id": post.id,
            "user": post.user.username,
            "content": post.content,
            "timestamp": post.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": 0
        }
    }, status=201)

@login_required
@require_http_methods(["GET", "PUT"])
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "GET":
        return JsonResponse({
            "id": post.id,
            "user": post.user.username,
            "content": post.content,
            "timestamp": post.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": post.likes.count(),
        })
    # PUT -> edit
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    if request.user != post.user:
        return HttpResponseForbidden("Cannot edit another user's post.")
    content = data.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "Content cannot be empty."}, status=400)
    if len(content) > 1000:
        return JsonResponse({"error": "Content too long."}, status=400)
    post.content = content
    post.save()
    return JsonResponse({"message": "updated", "content": post.content})

@login_required
@require_http_methods(["POST"])
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like = Like.objects.filter(user=request.user, post=post).first()
    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True
    return JsonResponse({"liked": liked, "likes": post.likes.count()})

@login_required
@require_http_methods(["POST"])
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if request.user == target:
        return JsonResponse({"error": "Cannot follow yourself."}, status=400)
    follow = Follow.objects.filter(follower=request.user, following=target).first()
    if follow:
        follow.delete()
        following = False
    else:
        Follow.objects.create(follower=request.user, following=target)
        following = True
    return JsonResponse({"following": following, "followers_count": target.followers_set.count()})

@login_required
def following_posts(request):
    following_ids = request.user.following_set.values_list("following_id", flat=True)
    posts_qs = Post.objects.filter(user__in=following_ids).select_related("user")
    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    user_likes = set(request.user.likes.values_list("post_id", flat=True))

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "user_likes": user_likes,
    })

def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts_qs = profile_user.posts.all()
    paginator = Paginator(posts_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    followers_count = profile_user.followers_set.count()
    following_count = profile_user.following_set.count()
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    user_likes = set()
    if request.user.is_authenticated:
        user_likes = set(request.user.likes.values_list("post_id", flat=True))

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
        "user_likes": user_likes,
    })