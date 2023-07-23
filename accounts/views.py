try:
    from django.utils import simplejson as json
except ImportError:
    import json

from django.db.models import Model

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.http import HttpResponse, JsonResponse

from .models import Account, Post, Coin

from accounts.forms import (
    RegistrationForm,
    AccountAuthenticationForm,
    PostForm,
    UserUpdateForm,
)

# Create your views here.

# User Registers Requests
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST, request.FILES)
        if form is not None:
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect("home")
        else:
            context["registration_form"] = form
    else:
        form = RegistrationForm()
        context["registration_form"] = form
    return render(request, "registration/register.html", context)


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")
    else:
        form = AccountAuthenticationForm()

    context["login_form"] = form
    return render(request, "registration/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def home(request):
    context = {}
    all_posts = Post.objects.all().order_by("-id")
    context["all_posts"] = all_posts
    return render(request, "home.html", context)


@login_required
def submit_post_view(request):
    context = {}
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect("/")
        else:
            form = PostForm()

        context["post_form"] = form

    return render(request, "submit_post.html", context)


@login_required
def leaderboard_view(request):
    context = {}
    users = Account.objects.all().order_by("-coins")
    context["users"] = users
    return render(request, "leaderboard.html", context)


@login_required
def profile_view(request, username):

    if username is not None:
        profile_user = Account.objects.filter(username=username).first()

        all_posts = Post.objects.all()
        all_posts = reversed(all_posts)
        users_posts = []
        user_total_posts = 0
        for post in all_posts:
            if profile_user == post.author:
                users_posts.append(post)
                user_total_posts = len(users_posts)

    else:
        profile_user = None

    context = {
        "profile_user": profile_user,
        "all_posts": users_posts,
        "user_total_posts": user_total_posts,
    }
    return render(request, "profile.html", context)


@login_required
def edit_profile_view(request, username):
    context = {}
    default_profile_image = "profile_images/default.jpg"

    if request.method == "POST":
        update_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            if request.user.profile_image == None:
                instance = Account.objects.filter(username=request.user)
                instance.save()
            else:
                update_form.save()
            return HttpResponseRedirect("/")

    else:
        update_form = UserUpdateForm(instance=request.user)

    context["update_form"] = update_form
    return render(request, "edit_profile.html", context)


@login_required
def like_view(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        total_likes = post.total_likes

        context = {"total_likes": total_likes}
        return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def follow_view(request, username):
    profile_user = Account.objects.filter(username=username).first()
    follow_logic = request.POST.get("follow_logic")

    if follow_logic == "Follow":
        follow = profile_user.followers.add(request.user)
        following = request.user.following.add(profile_user)
    else:
        unfollower = profile_user.followers.remove(request.user)
        unfollowing = request.user.following.remove(profile_user)

    followers = profile_user.followers.count()

    context = {
        "followers": followers,
        "follow_logic": follow_logic,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def delete_post_view(request, post_id):
    post_id = Post.objects.all().filter(id=post_id)
    post_id.delete()
    return HttpResponseRedirect("/")


@login_required
def quiz_view(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)

        question = post.question
        option1 = post.option1
        option2 = post.option2
        option3 = post.option3
        correct_answer = post.correct_answer
        context = {
            "question": question,
            "option1": option1,
            "option2": option2,
            "option3": option3,
            "correct_answer": correct_answer,
        }
        return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def quiz_score_view(request):
    if request.method == "POST":
        user = request.user
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        author = post.author
        user_choice = request.POST.get("quiz_option")
        correct_answer = post.correct_answer

        if user_choice == correct_answer:
            post.users_right.add(user)
            users_that_did_quiz = post.users_did_quiz.count()
            users_right_answer = post.users_right.count()
            coins = Coin.objects.get(id=1)
            total_coins = coins.network_coins

            total_coins = float(total_coins)
            coins_to_user = coins_user_get(
                users_that_did_quiz, users_right_answer, total_coins
            )
            coins_to_quiz_maker = coins_to_user * 0.05
            coins_to_user = coins_to_user - coins_to_quiz_maker
            account_of_user = Account.objects.get(username=user)
            account_of_quiz_maker = Account.objects.get(username=author)
            user_coins = float(account_of_user.coins)
            user_coins += coins_to_user
            account_of_user.coins = str(user_coins)
            account_of_user.save()
            author_coins = float(account_of_quiz_maker.coins)
            author_coins += coins_to_quiz_maker
            account_of_quiz_maker.coins = str(author_coins)
            account_of_quiz_maker.save()
            total_coins = total_coins - coins_to_user + coins_to_quiz_maker
            total_coins = str(total_coins)
            coins.network_coins = total_coins
            coins.save()
            user_right = True

        else:
            user_right = False
            coins_to_user = 0

        context = {
            "user_right": user_right,
            "coins_to_user": round(coins_to_user, 7),
        }

        return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def user_enter_quiz(request):
    if request.method == "POST":
        user = request.user
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        post.users_did_quiz.add(user)
        context = {}
        return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def post_comment(request):
    if request.method == "POST":
        print("puto")
        user = request.user
        comment = request.POST.get("comment")
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
     
        post.comments.add()

        total_comments = post.total_comments

        context = {"total_comments": total_comments}

        return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def clear_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.users_did_quiz.all().delete()
    return HttpResponseRedirect("/")


def coins_user_get(users_that_did_quiz, users_right_answer, total_coins):
    coins_to_user = (users_that_did_quiz / users_right_answer) / total_coins
    return coins_to_user

# @login_required
# def search_bar(request):
#     context = {"username": None}
#     if request.method == "POST":
#         username = request.POST.get("search_data")

#         for account in Account.objects.all():
#             if username == str(account):
#                 context["username"] = username

#         return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def drop_box(request):
    users = []
    if request.method == "POST":
        for accounts in Account.objects.all():
            usernames = str(accounts)
            users.append(usernames)

        context = {"users": users}
        return HttpResponse(json.dumps(context), content_type="application/json")



# Coin Utility!!!!
# oracion del dia, jesus vino a buscar la paz, pero no la encontró. Luego manu vino y le dio un besito. Amén
