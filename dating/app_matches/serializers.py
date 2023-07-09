from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Match
from services.match.match import MatchInterface


class MatchSerializer(serializers.Serializer):
    LIKE_CHOICES = (
        (True, "Like"),
        (False, "Dislike")
    )

    like_type = serializers.ChoiceField(
        choices=LIKE_CHOICES,
        style={'base_template': 'radio.html'},
    )

    def create(self, validated_data):
        sender_id = self.context.get('sender_id')
        receiver_id = self.context.get('receiver_id')
        flag, message = MatchInterface.create_match(sender_id, receiver_id)
        return flag, message

