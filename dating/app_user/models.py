from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from PIL import Image, ImageDraw


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
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
        Create and save a SuperUser with the given email and password.
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=CustomUser)
def add_watermark(sender, instance, **kwargs):
    if instance.avatar:
        avatar_image = Image.open(instance.avatar)
        watermark_image = Image.open(settings.MEDIA_ROOT / "watermark.png")

        watermark_width = int(avatar_image.width * 0.5)
        watermark_height = int(watermark_image.height * (watermark_width / watermark_image.width))
        watermark_image = watermark_image.resize((watermark_width, watermark_height))

        avatar_image.paste(watermark_image, (0, 0), watermark_image)

        avatar_image.save(instance.avatar.path)
