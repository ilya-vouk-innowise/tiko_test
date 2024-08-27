from datetime import datetime, timezone

from rest_framework.permissions import BasePermission


class IsCreatorOfEvent(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user == obj.creator
        )


class OnlyFutureEventRegistration(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ["register_for_event", "unregister_from_event"]:
            return bool(obj.start_date > datetime.now(tz=timezone.utc))
        return True
