from django.shortcuts import render, redirect
from study_buddy_app.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.template import loader

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
    print("2**************")
    print("request", request)
    print("room", room)
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'study_buddy_app/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    print("1**************")
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('http://localhost:8000/study_buddy_app/home/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('http://localhost:8000/study_buddy_app/home/'+room+'/?username='+username)

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




# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)