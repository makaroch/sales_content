from .forms import BinaryDocumentForm

from .models import Client, BinaryDocument, InputText, HelpChat, HelloMessage, PaySettings
from django.contrib import admin


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "is_paid_cheap_content",
        "is_paid_expensive_content",
        "date_create",
        "date_paid",
    ]


@admin.register(BinaryDocument)
class BinaryDocumentAdmin(admin.ModelAdmin):
    form = BinaryDocumentForm
    list_display = ['name', "download_link", "expansion", "status_file"]


@admin.register(InputText)
class InputTextAdmin(admin.ModelAdmin):
    pass


@admin.register(HelpChat)
class HelpChatAdmin(admin.ModelAdmin):
    list_display = ['message', "user_friendly_id"]


@admin.register(HelloMessage)
class HelloMessageAdmin(admin.ModelAdmin):
    list_display = ['message', "user_friendly_id"]


@admin.register(PaySettings)
class PaySettingsAdmin(admin.ModelAdmin):
    list_display = ['message', "btn_text", "price", "url", "user_friendly_id"]
