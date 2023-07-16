from rest_framework import serializers
from math import radians

from .models import CustomUser
from services.geo.geo import GeoInterface


class UserSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'gender',
            'avatar',
            'password',
            'longitude',
            'latitude',
            'distance',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'first_name': {'min_length': 2},
            'last_name': {'min_length': 2},
            'password': {'write_only': True,  'min_length': 8,
                         "style": {'input_type': 'password'}
                         },
            'longitude': {'read_only': True},
            'latitude': {'read_only': True},
        }

    def get_distance(self, obj):
        request_data = self.context['request'].data
        longitude_1 = request_data.get('longitude')
        latitude_1 = request_data.get('latitude')
        longitude_2 = obj.longitude
        latitude_2 = obj.latitude

        distance = GeoInterface.get_distance(longitude_1, latitude_1, longitude_2, latitude_2)
        return distance

    def create(self, validated_data):
        request_data = self.context['request'].data
        validated_data['longitude'] = request_data.get('longitude')
        validated_data['latitude'] = request_data.get('latitude')

        return super().create(validated_data)
