from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path("accounts/", include("allauth.urls")),
    path('logout', LogoutView.as_view()),

    path('deptlist/', views.deptlist, name="deptlist"),
    path('dept/<str:dept_name>/', views.dept, name="dept"),

    path('home/<str:room>/', views.room, name='room'),
    path('home/checkview', views.checkview, name='checkview'),
    path('home/send', views.send, name='send'),
    path('home/getMessages/<str:room>', views.getMessages, name='getMessages'),

    path('user/', views.user, name='user'),
    path('user/edituser/', views.edituser, name='edituser'),
    path('user/edituser/deptlist/', views.deptlist, name="deptlist"),
    path('user/edituser/dept/<str:dept_name>/', views.dept, name="dept"),
    path('user/edituser/dept/<str:dept_name>/addclass', views.addclass, name="addclass"),
]

