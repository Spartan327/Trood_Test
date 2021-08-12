from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('polls/', views.PollList.as_view()),
    path('polls/<int:pk>/', views.PollDetail.as_view()),
    path('polls/<int:pk>/questions/', views.QuestionList.as_view()),
    path('polls/<int:pk>/questions/<int:pk>/', views.QuestionDetail.as_view()),
    path('answers/', views.AnswerList.as_view()),
    path('answers/<int:pk>/', views.AnswerDetail.as_view()),
    path('votes/', views.VoteList.as_view()),
    path('votes/<int:pk>/', views.VoteDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
