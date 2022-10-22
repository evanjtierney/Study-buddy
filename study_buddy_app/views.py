from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import requests

def index(request):
    template = loader.get_template('study_buddy_app/home.html')
    context = {}
    return HttpResponse(template.render(context, request))


def sign_in(request):
    template = loader.get_template('study_buddy_app/google_login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def deptlist(request):
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    return render(request, 'study_buddy_app/deptlist.html', {'response':response})

def dept(request, dept_name):
    response = requests.get('http://luthers-list.herokuapp.com/api/dept/%s?format=json' %dept_name).json()
    return render(request, 'study_buddy_app/dept.html', {'response':response, 'dept_name':dept_name})  # , {'dept_name':dept_name}

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)