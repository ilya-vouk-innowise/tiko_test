from datetime import datetime, timedelta

from pytest import fixture

from events.models import Event


@fixture
def events_list(test_user):
    return Event.objects.bulk_create(
        [
            Event(
                name=f"Event {i}",
                description=f"Event {i} description",
                start_date=datetime(2024, 8, 27, 10, i, 5),
                end_date=datetime(2024, 8, 27, 11, i, 6),
                creator=test_user,
            )
            for i in range(5)
        ]
    )


@fixture
def test_event(test_user):
    return Event.objects.create(
        name="Test event",
        description="Test event description",
        start_date=datetime.now() + timedelta(days=5),
        end_date=datetime.now() + timedelta(days=6),
        creator=test_user,
    )


@fixture
def past_event(test_user):
    return Event.objects.create(
        name="Test event",
        description="Test event description",
        start_date=datetime.now() - timedelta(days=6),
        end_date=datetime.now() - timedelta(days=5),
        creator=test_user,
    )
