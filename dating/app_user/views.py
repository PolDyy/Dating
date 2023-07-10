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
        longitude, latitude = GeoInterface.get_coordinators(self.request)
        request.data['longitude'] = longitude
        request.data['latitude'] = latitude
        super().initial(request, *args, *kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        longitude, latitude = self.request.data['longitude'], self.request.data['latitude']
        context['longitude'] = longitude
        context['latitude'] = latitude
        return context
