from django.conf import settings
from django.core.mail import send_mail


class EmailSending:
    """Класс отправки сообщений."""

    DEFAULT_CONTENT = {
        "domain": "0.0.0.0:8000",
        "site_name": "Dating",
        "protocol": "http",
    }

    @classmethod
    def send_match_email(cls, email_to_sent: str, user_match_email: str, user_match_name: str):
        """Функция отправки сообщения о взаимной симпатии"""

        message = f"Вы понравились {user_match_name}! Почта участника: {user_match_email}"
        send_mail(
            "Вы кому-то понравились",
            message,
            settings.EMAIL_HOST_USER,
            [email_to_sent],
            fail_silently=True,
        )
