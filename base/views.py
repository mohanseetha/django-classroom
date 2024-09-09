from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(host__username__icontains=q) | Q(desc__icontains=q)) 
    rooms = rooms.filter(
        Q(branch__name=request.user.branch) & Q(year__yos=request.user.year) | Q(host__name=request.user.name)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'home.html', context)

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)  
    room_messages = room.message_set.all()
    followers = room.followers.all()

    if request.method=="POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        user = request.user
        room.followers.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'followers': followers}
    return render(request, 'room.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.get
    rooms = Room.objects.filter(
        Q(branch__name=request.user.branch) & Q(year__yos=request.user.year)
    )
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You\'re not authorized to edit the room')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    
    if request.user != room.host:
        return HttpResponse('You\'re not authorized to edit the room')
    
    context = {'obj': room}
    return render(request, 'delete.html', context)

def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
        except:
            messages.error(request, 'User doesn\'t exist')
    
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password isn\'t correct')

    context = {'page': page}
    return render(request, 'login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'login.html', {'form': form})

    
@login_required(login_url='login')
def deleteMsg(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == "POST":
        message.delete()
        return redirect('home')
    
    if request.user != message.user:
        return HttpResponse('You\'re not authorized to delete the message')
    
    context = {'obj': message}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
def editUser(request):
    user = request.user
    form = MyUserCreationForm(instance=user)
    if request.method == "POST":
        form = MyUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', user.id)
        
    context = {'form': form}
    return render(request, 'edit_user.html', context)

@login_required(login_url='login')
def topicsPage(request):
    topics = Topic.objects.all()
    context = {'topics': topics}
    return render(request, 'all_topics.html', context)

@login_required(login_url='login')
def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'all_activity.html', context)
