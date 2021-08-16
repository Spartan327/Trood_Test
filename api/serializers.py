from rest_framework import serializers
from .models import Answer, Poll, Question, Vote


class VoteSerializer(serializers.ModelSerializer):
    owner_id = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Vote
        fields = ['vote_id', 'owner_id', 'question', 'answer']


class AnswerSerializer(serializers.ModelSerializer):
    votes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ['answer_id', 'answer_text', 'votes']


class AnswerCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['answer_id']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerCountSerializer(many=True, read_only=True)
    votes_count = serializers.ReadOnlyField(source='count_votes')

    class Meta:
        model = Question
        fields = ['question_id', 'question_text', 'answers', 'votes_count']


class QuestionCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['question_id']


class PollSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    questions = QuestionCountSerializer(many=True, read_only=True)
    votes_count = serializers.ReadOnlyField(source='count_votes')

    class Meta:
        model = Poll
        fields = ['poll_id', 'owner', 'title', 'questions', 'votes_count']
