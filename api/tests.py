import pytest
import uuid

from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_view(client):
    url = 'http://127.0.0.1:8000/api/votes/'
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_superuser_view(admin_client):
    url = 'http://127.0.0.1:8000/admin/'
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.mark.django_db
def test_auth_view(client, create_user, test_password):
    user = create_user()
    url = 'http://127.0.0.1:8000/api-auth/login/'
    client.login(
        username=user.username, password=test_password
    )
    response = client.get(url)
    assert response.status_code == 200
