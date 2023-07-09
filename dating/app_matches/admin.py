from django.contrib import admin
from .models import Match


@admin.register(Match)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('get_sender_email', 'get_receiver_email')

    def get_sender_email(self, obj):
        return obj.sender.email

    def get_receiver_email(self, obj):
        return obj.receiver.email

    get_sender_email.short_description = 'Sender Email'
    get_receiver_email.short_description = 'Receiver Email'
