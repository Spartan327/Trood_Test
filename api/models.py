from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    poll_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=400, blank=False, null=False)
    owner = models.ForeignKey(
        User,
        related_name='polls',
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    def count_votes(self):
        question_list = list(self.questions.all())
        votes = 0
        for question in question_list:
            votes += question.votes.all().count()
        return votes

    class Meta:
        verbose_name_plural = 'Polls'
        verbose_name = 'Poll'
        ordering = ['poll_id']

    def __str__(self):
        return self.title


class Question(models.Model):
    question_id = models.BigAutoField(primary_key=True)
    question_text = models.TextField(
        blank=False,
        null=False)
    poll = models.ForeignKey(
        Poll,
        related_name='questions',
        on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User,
        related_name='questions',
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    def count_votes(self):
        answer_list = list(self.answers.all())
        votes = 0
        for answer in answer_list:
            votes += answer.votes.all().count()
        return votes

    class Meta:
        verbose_name_plural = 'Questions'
        verbose_name = 'Question'
        ordering = ['poll']

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    answer_id = models.BigAutoField(primary_key=True)
    answer_text = models.TextField(
        blank=False,
        null=False)
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User,
        related_name='answers',
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    class Meta:
        verbose_name_plural = 'Answers'
        verbose_name = 'Answer'
        ordering = ['question']

    def __str__(self):
        return self.answer_text


class Vote(models.Model):
    vote_id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='votes')
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='votes')
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='votes')

    def __str__(self):
        return self.owner.username
