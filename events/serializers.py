from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.models import Event, User


class EventAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class EventCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class EventSerializer(serializers.ModelSerializer):
    attendees = EventAttendeeSerializer(many=True, read_only=True)
    creator = EventCreatorSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "creator",
            "attendees",
        )

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if start_date or end_date:
            if not start_date or not end_date:
                raise ValidationError(
                    "Both start date and end date are required for update."
                )
            if start_date > end_date:
                raise ValidationError("Start date should not be after end date.")
        return data
