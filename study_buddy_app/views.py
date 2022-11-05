from django.shortcuts import render, redirect
from study_buddy_app.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import get_user_model
from django.views import generic

from django.shortcuts import render
import requests

from .models import Profile
from .forms import UserForm
from .models import Friends1
from .models import FriendRequest


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

##class viewProfiles(generic.ListView):
##    template_name = 'study_buddy_app/viewProfiles.html'
##    context_object_name = 'profile_list'
##    def get_queryset(self):
##        return Profile.objects.all()
    
def send_friend_request(request,pk):
    sender = request.user
    recipient = User.objects.get(id=pk)
    model = FriendRequest.objects.get_or_create(sender=request.user,receivers=recipient)
    return HttpResponse('friend request sent or already sent')
    #return redirect ('/study_buddy_app/user')

def delete_request(request, operation, pk):
    client1 = User.objects.get(id=pk)
    print(client1)
    if operation == 'Sender_deleting':
        model1 = FriendRequest.objects.get(sender=request.user, recievers=client1)
        model1.delete()
    elif operation == 'Reviever_deleting':
        model2 = FriendRequest.objects.get(sender=client1,receivers=request.user)
        model2.delete()
        return redirect('/studdy_buddy_app/user')
    return redirect('/study_buddy_app/user')

##def add_or_remove_friend(request,operation,pk):
##    new_friend = User.objects.get(id=pk)
##    if operation == 'add':
##        fq = FriendRequest.objects.get(sender=new_friend, recievers=request.user)
##        Friends1.make_friend(request.user, new_friend)
##        Friends1.make_friend(new_friend, request.user)
##        fq.delete()
##    elif operation == 'remove':
##        Friends1.lose_friend(request.user, new_friend)
##        Friends1.lose_friend(new_friend, request.user)
##    return redirect('/studdy_buddy_app/user')

def add_or_remove_friend(request,pk):
    new_friend = User.objects.get(id=pk)
    fq = FriendRequest.objects.get(sender=new_friend, recievers=request.user)
    Friends1.make_friend(request.user, new_friend)
    Friends1.make_friend(new_friend, request.user)
    fq.delete()
    #return redirect('/studdy_buddy_app/user')
    return('friend request accepted')

#new stuff
def publicProfile(request):
    user_form = UserForm(instance=request.user)
    return render(request = request, template_name ="study_buddy_app/publicProfile.html", context = {"user":request.user, "user_form": user_form})

class viewProfiles(generic.ListView):
    template_name = 'study_buddy_app/viewProfiles.html'
    context_object_name = 'profile_list'
    def get_queryset(self):
        return Profile.objects.all()

class listProfiles(generic.ListView):
    template_name = 'study_buddy_app/listProfiles.html'
    context_object_name = 'profile_list'
    def get_queryset(self):
        return Profile.objects.all()
    

class seeProfile(generic.DetailView):
    template_name = 'study_buddy_app/userProfile.html'
    context_object_name = 'profile_list'

    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    
def user_redirect(request):
    user = request.POST['username']

    return redirect('/study_buddy_app/publicProfile/'+user)

