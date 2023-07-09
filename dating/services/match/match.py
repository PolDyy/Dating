from app_matches.models import Match
from services.user.user import UserInterface
from services.smtp.smtp import EmailSending

from django.core.exceptions import ObjectDoesNotExist


class MatchInterface:
    """Класс управления симпатиями."""

    @staticmethod
    def create_match(sender_id: int, receiver_id: int) -> (bool, str):
        """Метод создания совпадения."""
        receiver_exist = UserInterface.check_user(receiver_id)

        if not receiver_exist:
            return False, "Пользователь не найден"

        try:
            match = Match.objects.select_related('sender', 'receiver')\
                .get(sender=receiver_id, receiver=sender_id)
            sender_email, sender_name = match.sender.email, match.sender.first_name
            receiver_email, receiver_name = match.receiver.email, match.receiver.first_name
            EmailSending.send_match_email(receiver_email, sender_email, sender_name)
            EmailSending.send_match_email(sender_email, receiver_email, receiver_name)
            return True, "У Вас взаимная симпатия! Проверяй почту ;)"
        except ObjectDoesNotExist:

            sender = UserInterface.get_user(sender_id)
            receiver = UserInterface.get_user(receiver_id)

            match = Match(sender=sender, receiver=receiver)
            match.save()

            return True, "Симпатия отправлена!"





