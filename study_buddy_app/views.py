from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the study_buddy_app index.")