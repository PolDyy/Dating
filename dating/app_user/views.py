from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from .models import CustomUser
from .serializers import UserSerializer


class UserViewSet(CreateModelMixin,
                  GenericViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
