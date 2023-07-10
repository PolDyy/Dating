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

        longitude_1 = radians(self.context.get('longitude'))
        latitude_1 = radians(self.context.get('latitude'))
        longitude_2 = obj.longitude
        latitude_2 = obj.latitude

        distance = GeoInterface.get_distance(longitude_1, latitude_1, longitude_2, latitude_2)
        return distance

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        gender = validated_data['gender']
        avatar = validated_data['avatar']
        password = validated_data['password']

        longitude = radians(self.context.get('longitude'))
        latitude = radians(self.context.get('latitude'))

        user = CustomUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            avatar=avatar,
            password=password,
            longitude=longitude,
            latitude=latitude,
        )

        return user
