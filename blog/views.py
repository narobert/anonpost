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
from blog.forms import UserForm, WPostForm, PPostForm, WCommentForm, PCommentForm
from blog.models import Wpost, Ppost, Profile, Wcomment, Pcomment, Wlike, Wdislike, Plike, Pdislike
from annoying.decorators import ajax_request
import simplejson as json


def home(request):
    total = 0
    wallposts = Wpost.objects.all().order_by("-id")
    wallcomments = Wcomment.objects.all().order_by("-id")
    friends = User.objects.all()
    needclick = Ppost.objects.filter(user2 = request.user.id, clicked = False)
    allposts = Ppost.objects.filter(user2 = request.user.id)
    for n in needclick:
        total = total + 1
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("home.html", {"user": request.user, "friends": friends, "wallposts": wallposts, "allposts": allposts, "total": total, "wallcomments": wallcomments})


def click(request, id):
    total = 0
    friends = User.objects.all()
    profileposts = Ppost.objects.get(id = id)
    profileposts.clicked = True
    profileposts.save()
    profilecomments = Pcomment.objects.filter(profile = profileposts).order_by("-id")
    needclick = Ppost.objects.filter(user2 = request.user.id, clicked = False)
    allposts = Ppost.objects.filter(user2 = request.user.id)
    for n in needclick:
        total = total + 1
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("click.html", {"user": request.user, "friends": friends, "profileposts": profileposts, "profilecomments": profilecomments, "allposts": allposts, "total": total})


def myprofile(request):
    total = 0
    friends = User.objects.all()
    profileposts = Ppost.objects.filter(user2 = request.user.id)
    profilecomments = Pcomment.objects.filter(profile = profileposts).order_by("-id")
    needclick = Ppost.objects.filter(user2 = request.user.id, clicked = False)
    allposts = Ppost.objects.filter(user2 = request.user.id)
    for n in needclick:
        total = total + 1
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("myprofile.html", {"user": request.user, "friends": friends, "profileposts": profileposts, "profilecomments": profilecomments, "allposts": allposts, "total": total})


def profile(request, username):
    total = 0
    if (Profile.objects.filter(user__username = username).count() == 0):
        return render_to_response("error.html")
    friends = User.objects.all()
    profileposts = Ppost.objects.filter(user2__username = username)
    profilecomments = Pcomment.objects.filter(profile = profileposts).order_by("-id")
    needclick = Ppost.objects.filter(user2 = request.user.id, clicked = False)
    allposts = Ppost.objects.filter(user2 = request.user.id)
    for n in needclick:
        total = total + 1
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("profile.html", {"user": request.user, "friends": friends, "username": username, "profileposts": profileposts, "profilecomments": profilecomments, "allposts": allposts, "total": total})


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


def commentwall(request, id):
    if request.method == 'POST':
        form = WCommentForm(request.POST)
        if form.is_valid():
            wallpost = Wpost.objects.get(id = id)
            if wallpost.hascomments == False:
                wallpost.hascomments = True
                wallpost.save()
            wallcomment = form.cleaned_data['wallcomment']
            createcomment = Wcomment.objects.create(user = request.user, wallcomment = wallcomment, wall = wallpost)
            createcomment.save()
            return HttpResponseRedirect('/')
    else:
        form = WCommentForm()
    return render_to_response("error.html", {"form": form})


@ajax_request
def getCommentsW(request):
    id = request.POST.get("id")
    wallpost = Wpost.objects.get(id=id)

    comments = Wcomment.objects.filter(wall = wallpost)
    wallcomments = [pl.for_json() for pl in comments]

    return {"status": "OK", "wallcomments": wallcomments}


@ajax_request
def likewall(request, id):
    wallpost = Wpost.objects.get(id = id)
    walllike = Wlike.objects.filter(user = request.user, wall = wallpost)
    walldislike = Wdislike.objects.filter(user = request.user, wall = wallpost)

    if walllike.count() == 0 and walldislike.count() == 0:
        createlike = Wlike.objects.create(user = request.user, wall = wallpost)
        wallpost.likes += 1
        wallpost.save()
        createlike.save()

    elif walllike.count() == 1 and walldislike.count() == 0:
        getlike = Wlike.objects.get(user = request.user, wall = wallpost)
        wallpost.likes -= 1
        wallpost.save()
        getlike.delete()

    elif walllike.count() == 0 and walldislike.count() == 1:
        getdislike = Wdislike.objects.get(user = request.user, wall = wallpost)
        createlike = Wlike.objects.create(user = request.user, wall = wallpost)
        wallpost.likes += 2
        wallpost.save()
        getdislike.delete()
        createlike.save()

    return HttpResponseRedirect('/')


@ajax_request
def dislikewall(request, id):
    wallpost = Wpost.objects.get(id = id)
    walldislike = Wdislike.objects.filter(user = request.user, wall = wallpost)
    walllike = Wlike.objects.filter(user = request.user, wall = wallpost)

    if walldislike.count() == 0 and walllike.count() == 0:
        createdislike = Wdislike.objects.create(user = request.user, wall = wallpost)
        wallpost.likes -= 1
        wallpost.save()
        createdislike.save()

    elif walldislike.count() == 1 and walllike.count() == 0:
        getdislike = Wdislike.objects.get(user = request.user, wall = wallpost)
        wallpost.likes += 1
        wallpost.save()
        getdislike.delete()

    elif walldislike.count() == 0 and walllike.count() == 1:
        getlike = Wlike.objects.get(user = request.user, wall = wallpost)
        createdislike = Wdislike.objects.create(user = request.user, wall = wallpost)
        wallpost.likes -= 2
        wallpost.save()
        getlike.delete()
        createdislike.save()

    return HttpResponseRedirect('/')


@ajax_request
def getLikesW(request):
    wallpost = Wpost.objects.all()
    walllikes = [pl.for_json() for pl in wallpost]

    return {"status": "OK", "walllikes": walllikes}


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


def commentprofile(request, id):
    if request.method == 'POST':
        form = PCommentForm(request.POST)
        if form.is_valid():
            profilepost = Ppost.objects.get(id = id)
            if profilepost.hascomments == False:
                profilepost.hascomments = True
                profilepost.save()
            profilecomment = form.cleaned_data['profilecomment']
            createcomment = Pcomment.objects.create(user = request.user, profilecomment = profilecomment, profile = profilepost)
            createcomment.save()
            url = reverse('profile', kwargs={'username': profilepost.user2.username})
            return HttpResponseRedirect(url)
    else:
        form = PCommentForm()
    return render_to_response("error.html", {"form": form})


def commentpost(request, id):
    if request.method == 'POST':
        form = PCommentForm(request.POST)
        if form.is_valid():
            profilepost = Ppost.objects.get(id = id)
            if profilepost.hascomments == False:
                profilepost.hascomments = True
                profilepost.save()
            profilecomment = form.cleaned_data['profilecomment']
            createcomment = Pcomment.objects.create(user = request.user, profilecomment = profilecomment, profile = profilepost)
            createcomment.save()
            url = reverse('click', kwargs={'id': id})
            return HttpResponseRedirect(url)
    else:
        form = PCommentForm()
    return render_to_response("error.html", {"form": form})


@ajax_request
def getCommentsP(request):
    id = request.POST.get("id")
    profilepost = Ppost.objects.get(id=id)

    comments = Pcomment.objects.filter(profile = profilepost)
    profilecomments = [pl.for_json() for pl in comments]

    return {"status": "OK", "profilecomments": profilecomments}


@ajax_request
def likeprofile(request, id):
    profilepost = Ppost.objects.get(id = id)
    profilelike = Plike.objects.filter(user = request.user, profile = profilepost)
    profiledislike = Pdislike.objects.filter(user = request.user, profile = profilepost)

    if profilelike.count() == 0 and profiledislike.count() == 0:
        createlike = Plike.objects.create(user = request.user, profile = profilepost)
        profilepost.likes += 1
        profilepost.save()
        createlike.save()

    elif profilelike.count() == 1 and profiledislike.count() == 0:
        getlike = Plike.objects.get(user = request.user, profile = profilepost)
        profilepost.likes -= 1
        profilepost.save()
        getlike.delete()

    elif profilelike.count() == 0 and profiledislike.count() == 1:
        getdislike = Pdislike.objects.get(user = request.user, profile = profilepost)
        createlike = Plike.objects.create(user = request.user, profile = profilepost)
        profilepost.likes += 2
        profilepost.save()
        getdislike.delete()
        createlike.save()

    url = reverse('click', kwargs={'id': id})
    return HttpResponseRedirect(url)


@ajax_request
def dislikeprofile(request, id):
    profilepost = Ppost.objects.get(id = id)
    profiledislike = Pdislike.objects.filter(user = request.user, profile = profilepost)
    profilelike = Plike.objects.filter(user = request.user, profile = profilepost)

    if profiledislike.count() == 0 and profilelike.count() == 0:
        createdislike = Pdislike.objects.create(user = request.user, profile = profilepost)
        profilepost.likes -= 1
        profilepost.save()
        createdislike.save()

    elif profiledislike.count() == 1 and profilelike.count() == 0:
        getdislike = Pdislike.objects.get(user = request.user, profile = profilepost)
        profilepost.likes += 1
        profilepost.save()
        getdislike.delete()

    elif profiledislike.count() == 0 and profilelike.count() == 1:
        getlike = Plike.objects.get(user = request.user, profile = profilepost)
        createdislike = Pdislike.objects.create(user = request.user, profile = profilepost)
        profilepost.likes -= 2
        profilepost.save()
        getlike.delete()
        createdislike.save()

    url = reverse('click', kwargs={'id': id})
    return HttpResponseRedirect(url)


@ajax_request
def getLikesP(request):
    profilepost = Ppost.objects.all()
    profilelikes = [pl.for_json() for pl in profilepost]

    return {"status": "OK", "profilelikes": profilelikes}


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
