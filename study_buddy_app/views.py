from django.shortcuts import render, redirect
from study_buddy_app.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import get_user_model

from django.shortcuts import render
import requests

from .models import Profile
from .forms import UserForm


def index(request):
    template = loader.get_template('study_buddy_app/home.html')
    context = {}
    return HttpResponse(template.render(context, request))


def sign_in(request):
    template = loader.get_template('study_buddy_app/google_login.html')
    context = {}
    return HttpResponse(template.render(context, request))
def home(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'study_buddy_app/chat.html', {'users': users})


def deptlist(request):
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    return render(request, 'study_buddy_app/deptlist.html', {'response':response})

def dept(request, dept_name):
    response = requests.get('http://luthers-list.herokuapp.com/api/dept/%s?format=json' %dept_name).json()
    return render(request, 'study_buddy_app/dept.html', {'response':response, 'dept_name':dept_name})  # , {'dept_name':dept_name}

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'study_buddy_app/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    sender = request.POST['username']
    sendee = request.POST['dropdown'] 
    array = [sender, sendee]
    array.sort()
    room = "".join([array[0], array[1]])
    if Room.objects.filter(name=room).exists():
        return redirect('/study_buddy_app/home/'+room+'/?username='+sender)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/study_buddy_app/home/'+room+'/?username='+sender)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


def user(request):
    user_form = UserForm(instance=request.user)
    return render(request = request, template_name ="study_buddy_app/user.html", context = {"user":request.user, "user_form": user_form})


def edituser(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, instance=request.user)
		if user_form.is_valid():
		    user_form.save()
	user_form = UserForm(instance=request.user)
	return render(request = request, template_name ="study_buddy_app/edituser.html", context = {"user":request.user,
		"user_form": user_form})
    
def publicProfile(request):
    user_form = UserForm(instance=request.user)
    return render(request = request, template_name ="study_buddy_app/publicProfile.html", context = {"user":request.user, "user_form": user_form})


    
