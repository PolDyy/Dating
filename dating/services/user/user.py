from rest_framework.request import Request
from django.core.exceptions import ObjectDoesNotExist

from app_user.models import CustomUser


class UserInterface:
    """Класс управления пользователями."""

    @staticmethod
    def get_user(id):
        try:
            user = CustomUser.objects.get(id=id)
            return user
        except ObjectDoesNotExist:
            return False

    @classmethod
    def get_user_data_for_match(cls, id: int, request: Request) -> dict or bool:
        user_exists = cls.check_user(id)
        if user_exists:
            user = CustomUser.objects.get(id=id)
            avatar = request.build_absolute_uri(user.avatar.url)
            data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "gender": user.gender,
                'avatar': avatar
            }
            return data
        return False

    @staticmethod
    def check_user(user_id: int) -> bool:
        """Метод проверки пользователя на существования."""
        user_exists = CustomUser.objects.filter(id=user_id).exists()

        if user_exists:
            return True

        return False
