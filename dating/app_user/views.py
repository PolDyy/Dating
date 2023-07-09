from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from .models import CustomUser
from .serializers import UserSerializer
from .filters import CustomUserFilter


class UserViewSet(ListModelMixin,
                  CreateModelMixin,
                  GenericViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filterset_class = CustomUserFilter
