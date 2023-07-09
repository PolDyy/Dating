from django_filters import rest_framework

from .models import CustomUser


class CustomUserFilter(rest_framework.FilterSet):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender']

