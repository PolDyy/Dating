from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from .models import CustomUser
from .serializers import UserSerializer
from .filters import CustomUserFilter
from services.geo.geo import GeoInterface


class UserViewSet(ListModelMixin,
                  CreateModelMixin,
                  GenericViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filterset_class = CustomUserFilter

    def initial(self, request, *args, **kwargs):
        longitude, latitude = GeoInterface.get_coordinators(request)
        request.data['longitude'] = longitude
        request.data['latitude'] = latitude
        super().initial(request, *args, **kwargs)

