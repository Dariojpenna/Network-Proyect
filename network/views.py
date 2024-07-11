from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm
from django.core.paginator import Paginator
from .models import User,Post,Followers,Like
from django.http import JsonResponse
import json
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Followers, Post
from django.shortcuts import redirect


def addLike(request,post_id):
    post = Post.objects.select_for_update().get(id=post_id)
    user = request.user
    post.like += 1
    post.save(update_fields=['like'])
    new_like = Like.objects.create(user=user, post=post)
    total_likes = Like.objects.filter(post=post).count()

    return JsonResponse({'message': "Like Added", 'total_likes': total_likes})

def removeLike(request,post_id):
    post = Post.objects.select_for_update().get(id=post_id)
    user = request.user
    post.like -=1
    post.save()
    like = Like.objects.get(user= user, post= post)
    like.delete()
    total_likes = Like.objects.filter(post=post).count()
    return JsonResponse({'message': "Like Removed", 'total_likes': total_likes})

def index(request):
    posts = Post.objects.order_by("-id")
    currentUser = request.user
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    postInPage = paginator.get_page(pageNumber)
    if currentUser.is_authenticated:
        likes = Like.objects.all().values_list('post_id', flat=True).filter(user=currentUser)
    else:
        likes = []
    all_users=User.objects.exclude(username =request.user.username)

    return render(request, "network/index.html",{
        "currentUser":currentUser,
        "postInPage": postInPage,
        "whoYouLiked": likes,
        "all_users": all_users
    })
    
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

def password_validation(password):
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)

    return has_upper and has_lower and has_digit

def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        country = request.POST["country"]
        if "profile_image" in request.FILES:
            profile_image = request.FILES["profile_image"]
        else:
            profile_image = None
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if not password_validation(password):
            return render(request, "network/register.html", {
                "message": "Password must contain at least one uppercase letter, one lowercase letter, and one digit."
            })
        if User.objects.filter(email=email).exists():
            return render(request, "network/register.html", {
                "message": "Email already taken."
            })
        elif password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,country=country,profile_image=profile_image,password=password)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def newPost(request):
    return render(request, "network/newPost.html",{
        "form":PostForm,
        "user": request.user 
    })

def addPost(request):
    postInPage = None
    if(request.method == "POST"):
        currentUser = request.user
        content = request.POST["postContent"]
        post = Post(post = content, user = currentUser)
        post.save()
        posts = Post.objects.all()
        posts = Post.objects.all().order_by("id").reverse()
        paginator = Paginator(posts, 10)
        pageNumber = request.GET.get('page')
        postInPage = paginator.get_page(pageNumber)
    return HttpResponseRedirect(reverse(index))
    
def profile(request,userConected):
    userProfile= User.objects.get(username=userConected)
    posts = Post.objects.filter(user=userProfile).order_by("id").reverse()
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    postInPage = paginator.get_page(pageNumber)
    following = Followers.objects.filter(userFollowed= userProfile.id)
    followers = Followers.objects.filter(userWhoFollows = userProfile.id)
    isFollower = False
    if request.user.is_authenticated:
        isFollower = followers.filter(userFollowed=  request.user)
    return render(request, "network/profile.html",{
        "currentUser":request.user,
        "postInPage":postInPage,
        "userProfile": userProfile,
        "following": following, 
        "followers":followers,
        "isFollower":isFollower
    })



def follow(request):
    user_to_follow = User.objects.get(username=request.POST['userFollow'])
    current_user = request.user
    Followers.objects.create(userWhoFollows=user_to_follow, userFollowed=current_user)
    return redirect('profile', userConected=user_to_follow.username)

def unfollow(request):
    userf = request.POST['userFollow']
    userFollow = User.objects.get(username=userf)
    currentUser = request.user
    Followers.objects.filter(userWhoFollows=userFollow, userFollowed=currentUser).delete()
    return HttpResponseRedirect(reverse(profile, kwargs={"userConected": userFollow.username}))



def following(request):
    followed_users = Followers.objects.filter(userFollowed=request.user)
    following_posts = Post.objects.filter(user__in=followed_users.values_list('userWhoFollows', flat=True)).order_by("-id")
    
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    posts_in_page = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "postInPage": posts_in_page,
    })
    

def edit(request,postId):
    if request.method == "POST":
        data = json.loads(request.body)
        post_content_edit = data.get('postContentEdit')
        post = Post.objects.get(id=postId)
        post.post= post_content_edit
        post.save()
        response_data = {
            'message': "Successful Modification",
            'postContentEdit': post_content_edit
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

