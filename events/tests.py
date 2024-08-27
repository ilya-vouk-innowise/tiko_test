from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user_model
from django.test import Client
from pytest import mark

from events.models import Event

User = get_user_model()


@mark.django_db
class TestEvents:
    def test_events_list(
        self, events_list: list[Event], client: Client, test_user: User
    ):
        res = client.get("/api/v1/events/")
        assert res.status_code == 200
        events_data = res.json()
        assert len(events_list) == len(events_data)

        event_data = events_data[0]
        event = [e for e in events_list if e.id == event_data["id"]][0]

        assert event_data["name"] == event.name
        assert event_data["description"] == event.description
        assert datetime.fromisoformat(
            event_data["start_date"]
        ) == event.start_date.replace(tzinfo=timezone.utc)
        assert datetime.fromisoformat(event_data["end_date"]) == event.end_date.replace(
            tzinfo=timezone.utc
        )
        assert event_data["creator"]["username"] == test_user.username

    def test_events_create_success(self, test_user_client: Client, test_user: User):
        res = test_user_client.post(
            path="/api/v1/events/",
            data={
                "name": "test_events_create",
                "description": "test_events_create",
                "start_date": (datetime.now() + timedelta(days=1)).isoformat(),
                "end_date": (datetime.now() + timedelta(days=1, hours=1)).isoformat(),
            },
        )
        assert res.status_code == 201

    def test_events_update_success(
        self, test_user_client: Client, test_user: User, test_event: Event
    ):
        new_data = {
            "name": "test_events_update_success",
            "description": "test_events_update_success",
            "start_date": (
                datetime.now(tz=timezone.utc) + timedelta(days=1)
            ).isoformat(),
            "end_date": (
                datetime.now(tz=timezone.utc) + timedelta(days=1, hours=1)
            ).isoformat(),
        }
        res = test_user_client.put(
            path=f"/api/v1/events/{test_event.id}/",
            data=new_data,
            content_type="application/json",
        )
        assert res.status_code == 200
        res_data = res.json()

        assert res_data["id"] == test_event.id
        assert res_data["name"] == new_data["name"]
        assert res_data["description"] == new_data["description"]
        assert datetime.fromisoformat(res_data["start_date"]) == datetime.fromisoformat(
            new_data["start_date"]
        )
        assert datetime.fromisoformat(res_data["end_date"]) == datetime.fromisoformat(
            new_data["end_date"]
        )

    def test_events_register_success(
        self, test_user_client: Client, test_user: User, test_event: Event
    ):
        assert test_user.events.count() == 0
        res = test_user_client.post(
            path=f"/api/v1/events/{test_event.id}/register/",
            data={},
            content_type="application/json",
        )
        assert res.status_code == 201
        assert test_user.events.count() == 1

    def test_events_register_past_event(
        self, test_user_client: Client, test_user: User, past_event: Event
    ):
        assert test_user.events.count() == 0
        res = test_user_client.post(
            path=f"/api/v1/events/{past_event.id}/register/",
            data={},
            content_type="application/json",
        )
        assert res.status_code == 403
        assert test_user.events.count() == 0

    def test_events_unregister_success(
        self,
        test_user_client: Client,
        test_user: User,
        test_event: Event,
    ):
        test_user.events.add(test_event)
        assert test_user.events.count() == 1
        res = test_user_client.post(
            path=f"/api/v1/events/{test_event.id}/unregister/",
            data={},
            content_type="application/json",
        )
        assert res.status_code == 204
        assert test_user.events.count() == 0

    def test_events_unregister_past_event(
        self,
        test_user_client: Client,
        test_user: User,
        past_event: Event,
    ):
        test_user.events.add(past_event)
        assert test_user.events.count() == 1
        res = test_user_client.post(
            path=f"/api/v1/events/{past_event.id}/unregister/",
            data={},
            content_type="application/json",
        )
        assert res.status_code == 403
        assert test_user.events.count() == 1
