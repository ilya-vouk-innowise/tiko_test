from django.test import Client
from pytest import mark

from registration.models import User


@mark.django_db
class TestRegistrationViews:
    def test_registration_success(self, client: Client):
        user_data = {
            "username": "test_registration_success",
            "email": "test_registration_success@example.com",
            "password": "test_registration_success",
        }
        res = client.post(path="/api/v1/register/", data=user_data)
        assert res.status_code == 201
        res_data = res.json()
        assert res_data == {
            "id": res_data["id"],
            "username": user_data["username"],
            "email": user_data["email"],
        }

    def test_registration_user_exists(self, client: Client, test_user: User):
        res = client.post(
            path="/api/v1/register/",
            data={"username": "test", "email": "test@example.com", "password": "test"},
        )
        assert res.status_code == 400
