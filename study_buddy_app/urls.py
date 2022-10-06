from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path("accounts/", include("allauth.urls")),
    path('logout', LogoutView.as_view()),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]