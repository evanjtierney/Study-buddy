from django.shortcuts import render, redirect
from study_buddy_app.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.template import loader
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
    return render(request, 'study_buddy_app/chat.html')

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
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/study_buddy_app/home/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/study_buddy_app/home/'+room+'/?username='+username)

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
	#if request.method == "POST":
	#	user_form = UserForm(request.POST, instance=request.user)
	#	if user_form.is_valid():
	#	    user_form.save()
		    #messages.success(request,('Your profile was successfully updated!'))
	#	else:
		    #messages.error(request,('Unable to complete request'))
                    #return redirect ("study_buddy_app:user")
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
