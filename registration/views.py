from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from registration.models import User
from registration.serializers import UserRegisterSerializer


class UserRegisterViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
