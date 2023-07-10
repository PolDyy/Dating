from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

from services.watermark import set_water_mark

class CustomUserManager(BaseUserManager):
    """
    Менеджер модели CustomUser определяющая email как уникальный ключ для аутентификации.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя по email и password.
        """
        if not email:
            raise ValueError('Поле Email должно быть заполнено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет супер-пользователя по email и password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', "Female")
    )
    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=CustomUser)
def add_watermark(sender, instance, **kwargs):
    """Сигнал для CustomUser, добавляющий к аватарке водный знак """
    if instance.avatar:
        avatar_image = Image.open(instance.avatar)
        avatar_image = set_water_mark(avatar_image)
        avatar_image.save(instance.avatar.path)
