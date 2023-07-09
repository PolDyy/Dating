from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'gender',
            'avatar',
            'password'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'first_name': {'min_length': 2},
            'last_name': {'min_length': 2},
            'password': {'write_only': True,  'min_length': 8,
                         "style": {'input_type': 'password'}
                         }
        }

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        gender = validated_data['gender']
        avatar = validated_data['avatar']
        password = validated_data['password']

        user = CustomUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            avatar=avatar,
            password=password,
        )

        return user
