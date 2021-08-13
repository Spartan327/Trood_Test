from django.db.models import query
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Answer, Poll, Question, Vote


class AnswerSerializer(serializers.ModelSerializer):
    votes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'votes']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    votes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answers', 'votes']


class PollSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'owner', 'title', 'created', 'questions']


class VoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Vote
        fields = ['id', 'owner', 'question', 'answer']
