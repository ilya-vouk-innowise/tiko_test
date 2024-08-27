from django.contrib.auth import get_user_model
from django.test import Client
from pytest import fixture

User = get_user_model()


@fixture
def test_user() -> User:
    return User.objects.create_user(username="test", password="test")


@fixture
def test_user_client(client: Client, test_user: User) -> Client:
    client.force_login(test_user)
    return client
