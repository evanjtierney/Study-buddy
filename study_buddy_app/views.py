from django.shortcuts import render, redirect, get_object_or_404
from study_buddy_app.models import Room, Message, Profile
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.db.models import Q # new
from django.views import generic
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View

from django.shortcuts import render
import requests

from .models import Profile, Class
from .forms import UserForm
from django import forms
from .models import Friends1
from .models import FriendRequest
#from .models import Class
from django.views import generic
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount

from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from datetime import datetime
from pytz import timezone
from allauth.socialaccount.models import SocialAccount
class SearchResultsView(generic.ListView):
    template_name = 'study_buddy_app/searchResults.html'
    context_object_name = 'search_results_list'
    def get_queryset(self):
        """Return all the users."""
        query = self.request.GET.get("q")
        User = get_user_model()
        users = User.objects.filter(Q(username__iexact=query) | Q(username__iexact=query))
        cardResults = []
        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)
        flag1 = not query is None and not has_numbers(query)
        flag2 = not query is None and has_numbers(query)
        

        if flag1:
            users |= User.objects.filter(Q(profile__classes__subject__iexact=query))

        if flag2:
            arr = query.split()
            if len(arr) == 2:
                users |= User.objects.filter(Q(profile__classes__subject__iexact=arr[0]) & Q(profile__classes__catalog_number__iexact=arr[1]))
        users = users.distinct()
        
        for user in users: 
            if flag1:
                cardResults.append(user.profile.classes.all().filter(Q(subject__iexact=query)))
            if flag2:
                cardResults.append(user.profile.classes.all().filter(Q(subject__iexact=arr[0]) & Q(catalog_number__iexact=arr[1])))
        print ("cardResults", cardResults)
        combination = zip(users, cardResults)
        return {'combination': combination}
    
    


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

# addclass API
def addclass_deptlist(request):
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    return render(request, 'study_buddy_app/addclassdeptlist.html', {'response':response})
# "
def dept(request, dept_name):
    classes = requests.get('http://luthers-list.herokuapp.com/api/dept/%s?format=json' %dept_name)
    response = classes.json()
    cur_classes = []
    for i in response:
        tmp = Class(subject=dept_name, catalog_number=i['catalog_number'], course_section=i['course_section'])
        tmp.save()
        cur_classes.append(tmp)
    return render(request, 'study_buddy_app/dept.html', {'response':cur_classes, 'dept_name':dept_name})

# display only API
def deptlist(request):
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    return render(request, 'study_buddy_app/deptlist.html', {'response':response})

# "
def dept_display_only(request, dept_name):
    classes = requests.get('http://luthers-list.herokuapp.com/api/dept/%s?format=json' %dept_name)
    response = classes.json()
    return render(request, 'study_buddy_app/deptdisplay.html', {'response':response, 'dept_name':dept_name})

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'study_buddy_app/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def go_to_chat(request):
    print('here!')
    sender = request.user.username
    sendee = request.POST['username'] 
    array = [sender, sendee]
    array.sort()
    room = "".join([array[0], array[1]])
    if Room.objects.filter(name=room).exists():
        return redirect('/study_buddy_app/home/'+room+'/?username='+sender)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/study_buddy_app/home/'+room+'/?username='+sender)

def checkview(request):
    room = ""
    sender = request.POST['username']
    sendee = request.POST.getlist('dropdown[]')
    array = [sender]

    for i in sendee:
        array.append(i)
    array.sort()

    for i in array:
        room = room + i

    if Room.objects.filter(name=room).exists():
        return redirect('/study_buddy_app/home/'+room+'/?username='+sender)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/study_buddy_app/home/'+room+'/?username='+sender)

def send(request):
    message = request.POST['message']
    if not message:
        return
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

    profile = Profile.objects.get(user=request.user)
    classes = profile.classes.all()
    return render(request = request, template_name ="study_buddy_app/user.html", context = {"user":request.user, "user_form": user_form, 'classes':classes})


def edituser(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
    user_form = UserForm(instance=request.user)

    # profile = Profile.objects.get(user=request.user)
    # classes = profile.classes.all()
    return render(request, 'study_buddy_app/edituser.html', context={'user':request.user, 'user_form':user_form})#, 'classes':classes})

def addclass(request):
    profile = Profile.objects.get(user=request.user)
    try:
        selected_class = Class.objects.get(pk=request.POST['class'])

        # only add class to profile if it's not already there
        already_exists = False
        for c in profile.classes.all():
            if selected_class.subject == c.subject and selected_class.catalog_number == c.catalog_number and selected_class.course_section == c.course_section:
                already_exists = True
        if not already_exists:
            profile.classes.add(selected_class)
            profile.save()

        return user(request)
    except(KeyError, Class.DoesNotExist):
        return render(request, 'study_buddy_app/dept.html', {
            'profile': profile,
            'error_message': "You didn't select a class.",
        })
        
def publicProfile(request):
    user_form = UserForm(instance=request.user)
    return render(request = request, template_name ="study_buddy_app/publicProfile.html", context = {"user":request.user, "user_form": user_form})

##class viewProfiles(generic.ListView):
##    template_name = 'study_buddy_app/viewProfiles.html'
##    context_object_name = 'profile_list'
##    def get_queryset(self):
##        return Profile.objects.all()
    
def send_friend_request(request,slug):
    sender = request.user
    recipient = User.objects.get(username = slug)
    model = FriendRequest.objects.get_or_create(sender=request.user,receiver=recipient)
    return HttpResponse('friend request sent or already sent')
    return redirect ('/study_buddy_app/publicProfile/'+user)
    #return redirct('/study_buddy_app/search_resulsts/publicProfile/<slug:slug>/')

def delete_request(request, pk):
    client1 = User.objects.get(username=pk)
    #print(client1)
    #if operation == 'Sender_deleting':
    #    model1 = FriendRequest.objects.get(sender=request.user, recievers=client1)
     #   model1.delete()
    #elif operation == 'Reviever_deleting':
    model2 = FriendRequest.objects.get(sender=client1,receiver=request.user)
    model2.delete()
    #return HttpResponse('Request Deleted')
    return redirect('/study_buddy_app/user/friend_request/')


def remove_friend(request, pk):
    new_friend = User.objects.get(username=pk)
    Friends1.lose_friend(request.user, new_friend)
    Friends1.lose_friend(new_friend, request.user)
    #return HttpResponse('friend removed')
    return redirect('/study_buddy_app/user/friends/')
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

def accept_friend_request(request,pk):
    new_friend = User.objects.get(username = pk)
    fq = FriendRequest.objects.get(sender=new_friend, receiver=request.user)
    Friends1.make_friend(request.user, new_friend)
    Friends1.make_friend(new_friend, request.user)
    fq.delete()
    #return redirect('/studdy_buddy_app/user')
    #return HttpResponse('friend request accepted')
    return redirect('/study_buddy_app/user/friend_request/')

##
##class viewProfiles(generic.ListView):
##    template_name = 'study_buddy_app/viewProfiles.html'
##    context_object_name = 'profile_list'
##    def get_queryset(self):
##        return Profile.objects.all()

class viewRequest(generic.ListView):
    template_name = 'study_buddy_app/friendRequest.html'
    context_object_name = 'request_list'
    def get_queryset(self):
        return FriendRequest.objects.filter(receiver = self.request.user)
    
class viewFriends(generic.ListView):
    template_name = 'study_buddy_app/friends.html'
    context_object_name = 'friend_list'
    def get_queryset(self):
        return Friends1.objects.filter(users1 = self.request.user)
    
#new stuff
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
    
class DateForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))
    start_time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time'}))
    end_time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time'}))

class seeProfile(generic.DetailView):

    model = Profile

    def get_context_data(self, **kwargs):
        context = super(seeProfile, self).get_context_data(**kwargs)
        context['form'] = DateForm()
        return context

class ProfileMeeting(SingleObjectMixin, FormView):
    template_name = 'study_buddy_app/profile_detail.html'
    form_class = DateForm
    model = Profile

    def form_valid(self, form):
        self.process_user_input(form.cleaned_data)
        return super(ProfileMeeting, self).form_valid(form)
    
    def process_user_input(self, valid_data):
        # TODO: add to google calendar
        # TODO: add this meeting time to the model
        
        def generate_credentials():
            token = SocialToken.objects.get(account__user__username=self.request.user.username, app__provider="google")

            credentials = Credentials(
                token=token.token,
                refresh_token=token.token_secret,
                token_uri='https://oauth2.googleapis.com/token',
                client_id='562188647966-r0odsb07scpsnj3jr8hfcu7912jeke61.apps.googleusercontent.com', # replace with yours 
                client_secret='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') # replace with yours 
            service = build('calendar', 'v3', credentials=credentials)
        
            return service
        
        def create_google_calendar_event(date, start_time, end_time, profile_user):
            event = {
                'summary': 'Study buddy meeting',
                # TODO: generate zoom meeting
                'location': 'Zoom link: ',
                # TODO: put person's name in the profile and the class
                'description': 'You have a study meeting with '+str(profile_user.first_name) + " "+str(profile_user.last_name),
                'start': {
                    'dateTime': str(date)+"T"+str(start_time),
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'dateTime': str(date)+"T"+str(end_time),
                    'timeZone': 'America/New_York',
                },
                'attendees': [
                    {'email': profile_user.email},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
        
        def add_event_to_calendar(date, start_time, end_time, profile_user):
            eastern = timezone('US/Eastern')
            start_datetime = datetime.combine(date, start_time, eastern)
            end_datetime = datetime.combine(date, end_time, eastern)

            event = Event(title="Meeting w/"+profile_user.username,
                            description="Meeting with "+profile_user.first_name+" "+profile_user.last_name,
                            start_time=start_datetime,
                            end_time=end_datetime)
            event.save()

            self.request.user.event_set.add(event)
            print("self.request.user events", self.request.user.event_set.all())
           
            copy = Event(title="Meeting w/"+self.request.user.username,
                            description="Meeting with "+self.request.user.first_name+" "+self.request.user.last_name,
                            start_time=start_datetime,
                            end_time=end_datetime)
            copy.save()
            
            profile_user.event_set.add(copy)
            print("profile_user events", profile_user.event_set.all())
        
        profile_user = User.objects.get(profile__slug=self.kwargs['slug'])
        
        googleSet = SocialAccount.objects.filter(provider="google")
        requestUser_isGoogle = len(googleSet.filter(user=self.request.user)) > 0
        
        profileUser_isGoogle = len(googleSet.filter(user=profile_user)) > 0
        
        if requestUser_isGoogle and profileUser_isGoogle:
            service = generate_credentials()
            create_google_calendar_event(valid_data['date'], valid_data['start_time'], valid_data['end_time'], profile_user)

        add_event_to_calendar(valid_data['date'], valid_data['start_time'], valid_data['end_time'], profile_user)
    
        pass

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('profile-detail', kwargs={'slug': self.object.slug})

class ProfileDetail(View):
    template_name = 'study_buddy_app/profile_detail.html'
    def get(self, request, *args, **kwargs):
        view = seeProfile.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProfileMeeting.as_view()
        return view(request, *args, **kwargs)

def user_redirect(request):
    user = request.POST['username']
    user_obj = User.objects.get(username=user)
    if user_obj.username == request.user.username:
        return redirect('/study_buddy_app/user/')
    return redirect('/study_buddy_app/publicProfile/'+user)

class CalendarView(generic.ListView):
    model = Event
    template_name = 'study_buddy_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request.user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
