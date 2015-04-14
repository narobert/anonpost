# Create your views here.
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django import forms
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from blog.forms import UserForm, WPostForm, PPostForm
from blog.models import Wpost, Ppost, Profile


def home(request):
    total = 0
    wallposts = Wpost.objects.all()
    friends = User.objects.all()
    needclick = Ppost.objects.filter(user2 = request.user.id, clicked = False)
    allposts = Ppost.objects.filter(user2 = request.user.id)
    for n in needclick:
        total = total + 1
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("home.html", {"user": request.user, "friends": friends, "wallposts": wallposts, "allposts": allposts, "total": total})


def click(request, id):
    total = 0
    friends = User.objects.all()
    profileposts = Ppost.objects.get(id = id)
    profileposts.clicked = True
    profileposts.save()
    needclick = Ppost.objects.filter(user2 = request.user.id, clicked = False)
    allposts = Ppost.objects.filter(user2 = request.user.id)
    for n in needclick:
        total = total + 1
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("click.html", {"user": request.user, "friends": friends, "profileposts": profileposts, "allposts": allposts, "total": total})


def myprofile(request):
    total = 0
    friends = User.objects.all()
    profileposts = Ppost.objects.filter(user2 = request.user.id)
    needclick = Ppost.objects.filter(user2 = request.user.id, clicked = False)
    allposts = Ppost.objects.filter(user2 = request.user.id)
    for n in needclick:
        total = total + 1
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("myprofile.html", {"user": request.user, "friends": friends, "profileposts": profileposts, "allposts": allposts, "total": total})


def profile(request, username):
    total = 0
    if (Profile.objects.filter(user__username = username).count() == 0):
        return render_to_response("error.html")
    friends = User.objects.all()
    profileposts = Ppost.objects.filter(user2__username = username)
    needclick = Ppost.objects.filter(user2 = request.user.id, clicked = False)
    allposts = Ppost.objects.filter(user2 = request.user.id)
    for n in needclick:
        total = total + 1
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("profile.html", {"user": request.user, "friends": friends, "username": username, "profileposts": profileposts, "allposts": allposts, "total": total})


def postwall(request):
    if request.method == 'POST':
        form = WPostForm(request.POST)
        if form.is_valid():
            wallpost = form.cleaned_data['wallpost']
            createpost = Wpost.objects.create(user = request.user, wallpost = wallpost)
            createpost.save()
            return HttpResponseRedirect('/')
    else:
        form = WPostForm()
    return render_to_response("error.html", {"form": form})


def postprofile(request, username):
    if request.method == 'POST':
        form = PPostForm(request.POST)
        if form.is_valid():
            profilepost = form.cleaned_data['profilepost']
            profile = Profile.objects.get(user__username = username)
            createpost = Ppost.objects.create(user1 = request.user, user2 = profile.user, profilepost = profilepost)
            createpost.save()
            return HttpResponseRedirect('/profile/' + username + '/')
    else:
        form = PPostForm()
    return render_to_response("error.html", {"form": form})


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            newuser = User.objects.create_user(name, form.cleaned_data['email'], pw)
            newuser.save()
            profile = Profile.objects.create(user = newuser)
            profile.save()
            user = authenticate(username = name, password = pw)
            auth_login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
    return render_to_response("register.html", {'form':form})


def login(request):
    username = password = ''
    error = False
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
  
        user = authenticate(username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = True
    return render_to_response("login.html", {'error': error})
  

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
