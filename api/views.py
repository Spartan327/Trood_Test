from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response


from .models import Answer, Poll, Question, Vote
from .permisisions import IsOwnerOrReadOnly
from .serializers import AnswerSerializer, PollSerializer, QuestionSerializer, VoteSerializer


class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    lookup_field = 'poll_id'


class QuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'poll_id'

    def perform_create(self, serializer):
        poll = Poll.objects.get(poll_id=self.kwargs["poll_id"])
        serializer.save(owner=self.request.user, poll=poll)

    def get_queryset(self):
        queryset = Question.objects.filter(poll_id=self.kwargs["poll_id"])
        return queryset


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    lookup_field = 'question_id'

    def get_queryset(self):
        queryset = Question.objects.all().filter(
            question_id=self.kwargs["question_id"]
            )
        return queryset


class AnswerList(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'question_id'

    def perform_create(self, serializer):
        question = Question.objects.get(question_id=self.kwargs["question_id"])
        serializer.save(owner=self.request.user, question=question)

    def get_queryset(self):
        queryset = Answer.objects.all().filter(
            question_id=self.kwargs["question_id"])
        return queryset


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    lookup_field = 'answer_id'

    def get_queryset(self):
        queryset = Answer.objects.all().filter(
            answer_id=self.kwargs["answer_id"]
            )
        return queryset


class VoteList(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        question_id = request.data['question']
        answer_id = request.data['answer']
        if request.user.is_anonymous:
            csrftoken = request.COOKIES['csrftoken']
            anonymous_user = User.objects.filter(username=csrftoken).first()
            if not anonymous_user:
                anonymous_user = User.objects.create_user(
                    username=csrftoken,
                    email=None,
                    password=None)
                anonymous_user.save()
            request.user = anonymous_user
        user_id = request.user.id
        list_answers_id = []
        for answer in list(Question.objects.get(question_id=question_id).answers.all().values('answer_id')):
            list_answers_id.append(answer['answer_id'])
        if int(answer_id) in list_answers_id:
            vote = Vote.objects.filter(
                owner_id=user_id,
                question_id=question_id).first()
            if not vote:
                return super().create(request, *args, **kwargs)
            return Response(
                {'message': 'Вы уже отвечали на данный вопрос'},
                status=status.HTTP_403_FORBIDDEN,
                headers=None)
        return Response(
            {'message': 'Выбраный ответ не соответствует вопросу'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers=None)
