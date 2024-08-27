from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from events.filters import EventFilter
from events.models import Event
from events.permissions import IsCreatorOfEvent, OnlyFutureEventRegistration
from events.serializers import EventSerializer


class EventViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsCreatorOfEvent,
        OnlyFutureEventRegistration,
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @extend_schema(request=None)
    @action(
        detail=True,
        methods=["POST"],
        url_path="register",
        serializer_class=EventSerializer,
    )
    def register_for_event(self, request, *args, **kwargs):
        event = self.get_object()
        if not event:
            return Response(data={"detail": "Event not found."}, status=404)
        event.attendees.add(request.user)
        return Response(
            data={"detail": "Successfully registered for the event."}, status=201
        )

    @extend_schema(request=None)
    @action(detail=True, methods=["POST"], url_path="unregister")
    def unregister_from_event(self, request, *args, **kwargs):
        event = self.get_object()
        if not event:
            return Response(data={"detail": "Event not found."}, status=404)
        event.attendees.remove(request.user)
        return Response(
            data={"detail": "Successfully unregistered from the event."}, status=204
        )
