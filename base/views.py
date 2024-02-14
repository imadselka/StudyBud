from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from base.forms import RoomForm
from .models import Room, Topic, Message, User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Message


# Create your views here.
def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        print(username, password)
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "ERROR: user name was not found.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "ERROR: username or password is incorrect.")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutPage(request):
    logout(request)
    return redirect("home")


from django.contrib.auth.forms import UserCreationForm  # Import the UserCreationForm


def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "ERROR: an error occurred during registration.")
    context = {"form": form}
    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    if not rooms.exists():
        return render(request, "base/error.html")

    room_count = rooms.count()
    # icontains is case insensitive
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


from .models import Message  # Import the Message model


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = Message.objects.filter(room=room).order_by("-created")
    participants = room.participants.all()
    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body"),
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.pk)
    return render(request, "base/room.html", context)


from .models import Room  # Import the Room model


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = Room.objects.filter(host=user)
    room_messages = Message.objects.filter(user=user).order_by("-created")
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form, "is_creating_room": True}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form, "is_creating_room": False}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    # obj is the object to be deleted we use obj in html file
    context = {"obj": room}
    return render(request, "base/delete.html", context)


from django.http import HttpResponseRedirect  # Import the HttpResponseRedirect module


from django.shortcuts import render, HttpResponseRedirect


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponseRedirect("You are not allowed here!")

    if request.method == "POST":
        referer = request.session.get("referer", "/")
        message.delete()
        return HttpResponseRedirect(referer)

    # Store the referer URL in session
    request.session["referer"] = request.META.get("HTTP_REFERER")

    context = {"obj": message}
    return render(request, "base/delete.html", context)


from .forms import MessageForm  # Import the MessageForm class


@login_required(login_url="login")
def updateMessage(request, pk):
    message = Message.objects.get(id=pk)
    form = MessageForm(instance=message)  # Fix: Replace `Message` with `MessageForm`

    if request.user != message.user:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        form = MessageForm(
            request.POST, instance=message
        )  # Fix: Close the opening parenthesis after `form =` and remove the unnecessary opening parenthesis before `request.POST`
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form, "is_updating_message": True}
    return render(request, "base/room_form.html", context)
