from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('polls/', views.PollList.as_view()),
    path('polls/<int:poll_id>/', views.PollDetail.as_view()),
    path('polls/<int:poll_id>/questions/', views.QuestionList.as_view()),
    path('polls/<int:poll_id>/questions/<int:question_id>/', views.QuestionDetail.as_view()),
    path('polls/<int:poll_id>/questions/<int:question_id>/answers/', views.AnswerList.as_view()),
    path('polls/<int:poll_id>/questions/<int:question_id>/answers/<int:answer_id>/', views.AnswerDetail.as_view()),
    path('votes/', views.VoteList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
