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
    #path('publicProfile/', views.publicProfile, name='publicProfile'),
    #path('publicProfile/viewAll', views.viewProfiles.as_view(), name='viewAll'),
    path('user/', views.user, name='user'),
    path('user/edituser/', views.edituser, name='edituser'),
    #path('/publicProfile/viewAll/send_friend_request/<int:userID>/',views.send_friend_request,name='send friend request'),
    path('publicProfile/', views.publicProfile, name='publicProfile'),

    path('publicProfile/viewAll', views.viewProfiles.as_view(), name='viewAll'),
    
    path('publicProfile/listProfiles', views.listProfiles.as_view(), name='listProfiles'),

    path('publicProfile/user_redirect/', views.user_redirect, name='user_redirect'),

    path('publicProfile/<slug:slug>/', views.seeProfile.as_view(), name='profile-detail'),

    path('publicProfile/<slug:slug>/study_buddy_app/send_friend_request/', views.send_friend_request,name='send friend request'),
    
    path('user/friends', views.viewFriends.as_view(), name='new_friends'),

    path('user/friend_request/', views.viewRequest.as_view(), name='requests'),

    path('user/friend_request/accept_friend_request/<str:pk>/', views.accept_friend_request, name='accept friend request'),


]

