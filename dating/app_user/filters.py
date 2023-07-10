from django_filters import rest_framework as filters
from math import radians
from django.core import validators

from services.geo.geo import GeoInterface
from .models import CustomUser


class CustomUserFilter(filters.FilterSet):
    distance = filters.NumberFilter(field_name="distance", method='fiter_by_distance',
                                    validators=[validators.MinValueValidator(0)], label='Distance')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender']

    def fiter_by_distance(self, queryset, name, value):

        longitude_1 = radians(self.request.data.get('longitude'))
        latitude_1 = radians(self.request.data.get('latitude'))
        cords = GeoInterface.calculate_coordinates_in_directions(latitude_1, longitude_1, float(value))
        latitudes = cords['latitude']
        longitudes = cords['longitude']
        queryset = queryset.filter(
            longitude__gte=longitudes[1], longitude__lte=longitudes[0],
            latitude__gte=latitudes[1], latitude__lte=latitudes[0]
        )
        return queryset
