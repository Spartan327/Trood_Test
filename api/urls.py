from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('polls/', views.PollList.as_view()),
    path('polls/<int:pk>/', views.PollDetail.as_view()),
    path('polls/<int:pk>/questions/', views.QuestionList.as_view()),
    path('polls/<int:pk>/questions/<int:id>/', views.QuestionDetail.as_view()),
    path('polls/<int:pk>/questions/<int:id>/answers/', views.AnswerList.as_view()),
    path('polls/<int:pk>/questions/<int:id>/answers/<int:question_id>/', views.AnswerDetail.as_view()),
    path('votes/', views.VoteList.as_view()),
    path('votes/<int:pk>/', views.VoteDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
