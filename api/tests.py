import json

import pytest
import uuid

from django.urls import reverse
from api.models import Poll, Question, Answer, Vote


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.mark.django_db
def test_polls_request(api_client):
    url = reverse('polls')
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_poll_create(api_client, create_user, test_password):
    test_user = create_user()
    data = {'title': 'test poll'}
    url = reverse('polls')
    api_client.login(
        username=test_user.username, password=test_password)
    response = api_client.post(
        url,
        data=json.dumps(data),
        content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_poll_detail_request(api_client, create_user):
    test_user = create_user()
    test_poll = Poll.objects.create(title='test poll', owner=test_user)
    url = reverse('polls_detail', kwargs={'poll_id': test_poll.poll_id})
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_poll_put(api_client, create_user, test_password):
    test_user = create_user()
    test_poll = Poll.objects.create(title='test poll', owner=test_user)
    api_client.login(
        username=test_user.username, password=test_password
    )
    data = {
        'poll_id': test_poll.poll_id,
        'owner': test_poll.owner.username,
        'title': 'test_new_title',
        'questions': list(test_poll.questions.all().values('question_id')),
        'votes_count': test_poll.count_votes()}
    url = reverse('polls_detail', kwargs={'poll_id': test_poll.poll_id})
    response = api_client.put(
        url,
        data=json.dumps(data),
        content_type='application/json')
    assert response.data['title'] == 'test_new_title'


@pytest.mark.django_db
def test_poll_delete(api_client, create_user, test_password):
    test_user = create_user()
    test_poll = Poll.objects.create(title='test poll', owner=test_user)
    api_client.login(
        username=test_user.username, password=test_password
    )
    data = {'poll_id': test_poll.poll_id}
    print(json.dumps(data))
    url = reverse('polls_detail', kwargs={'poll_id': test_poll.poll_id})
    response = api_client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_question_create(api_client, create_user, test_password):
    test_user = create_user()
    test_poll = Poll.objects.create(title='test poll', owner=test_user)
    data = {'question_text': 'test question'}
    url = reverse('questions', kwargs={'poll_id': test_poll.poll_id})
    api_client.login(
        username=test_user.username, password=test_password)
    response = api_client.post(
        url,
        data=json.dumps(data),
        content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_qestion_detail_request(api_client, create_user):
    test_user = create_user()
    test_poll = Poll.objects.create(title='test_poll', owner=test_user)
    test_qestion = Question.objects.create(
        question_text='test qestion', owner=test_user, poll=test_poll)
    url = reverse('question_detail', kwargs={
                  'poll_id': test_poll.poll_id, 'question_id': test_qestion.question_id})
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_votes_request(api_client):
    url = reverse('votes')
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_vote_create(api_client, create_user, test_password):
    test_user = create_user()
    test_poll = Poll.objects.create(title='test_poll', owner=test_user)
    test_qestion = Question.objects.create(
        question_text='test qestion', owner=test_user, poll=test_poll)
    test_answer = Answer.objects.create(
        answer_text='test qestion', owner=test_user, question=test_qestion)
    data = {'question': test_qestion.question_id,
            'answer': test_answer.answer_id}
    url = reverse('votes')
    test_another_user = create_user()
    api_client.login(
        username=test_another_user.username, password=test_password)
    response = api_client.post(
        url,
        data=json.dumps(data),
        content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_vote_another_answer_question_create(api_client, create_user, test_password):
    test_user = create_user()
    test_poll = Poll.objects.create(title='test_poll', owner=test_user)
    test_qestion = Question.objects.create(
        question_text='test qestion', owner=test_user, poll=test_poll)
    test_another_qestion = Question.objects.create(
        question_text='test another qestion', owner=test_user, poll=test_poll)
    test_another_answer = Answer.objects.create(
        answer_text='test another answer', owner=test_user, question=test_another_qestion)
    data = {'question': test_qestion.question_id,
            'answer': test_another_answer.answer_id}
    url = reverse('votes')
    test_another_user = create_user()
    api_client.login(
        username=test_another_user.username, password=test_password)
    api_client.login(
        username=test_user.username, password=test_password)
    response = api_client.post(
        url,
        data=json.dumps(data),
        content_type='application/json')
    assert response.status_code == 422


@pytest.mark.django_db
def test_one_answer_vote_create(api_client, create_user, test_password):
    test_user = create_user()
    test_poll = Poll.objects.create(title='test_poll', owner=test_user)
    test_qestion = Question.objects.create(
        question_text='test qestion', owner=test_user, poll=test_poll)
    test_answer = Answer.objects.create(
        answer_text='test qestion', owner=test_user, question=test_qestion)
    test_another_user = create_user()
    Vote.objects.create(
        owner=test_another_user, question=test_qestion, answer=test_answer)
    data = {'question': test_qestion.question_id,
            'answer': test_answer.answer_id}
    url = reverse('votes')
    api_client.login(
        username=test_another_user.username, password=test_password)
    response = api_client.post(
        url,
        data=json.dumps(data),
        content_type='application/json')
    assert response.status_code == 403
