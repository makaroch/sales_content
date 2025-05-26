from datetime import datetime

from django.db import models
from django.utils.html import format_html
from django.urls import reverse


class Status(models.TextChoices):
    FREE = 'FREE', 'Бесплатный контент'
    RASS = 'RASS', 'Рассылка'


class Client(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=False, verbose_name="Телеграм ID")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    is_paid_cheap_content = models.BooleanField(default=False, verbose_name="Оплачен дешевый контент")
    is_paid_expensive_content = models.BooleanField(default=False, verbose_name="Оплачен дорогой контент")
    date_create = models.DateTimeField(default=datetime.now, verbose_name="Дата создания")
    date_paid = models.DateTimeField(null=True, blank=True, verbose_name="Дата оплаты")
    # time_paid = models.DateTimeField(null=True, blank=True, verbose_name="Время оплаты")

    def __str__(self):
        return f"Клиент: {self.username} | {self.id} | {self.is_paid_cheap_content} | {self.is_paid_expensive_content}"

    class Meta:
        db_table = "clients"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class BinaryDocument(models.Model):
    name = models.CharField(max_length=255)
    expansion = models.CharField(max_length=10)
    status_file = models.CharField(max_length=10, choices=Status.choices, default=Status.FREE)
    file_data = models.BinaryField()  # содержимое файла будет храниться прямо в Postgre

    def __str__(self):
        return f"Документ {self.name}"

    class Meta:
        db_table = "documents"
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def download_link(self):
        url = reverse('admin_download_file', args=[self.pk])
        return format_html('<a href="{}" download>Скачать</a>', url)

    download_link.short_description = "Файл"


class InputText(models.Model):
    text_input = models.TextField("Введите текст", blank=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Текст: {self.text_input} | {self.id} | {self.date_create}"

    class Meta:
        db_table = "spam_messages"
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылка"


class PaySettings(models.Model):
    message = models.TextField(verbose_name="Сообщение")
    btn_text = models.CharField(max_length=255, verbose_name="Текст кнопки")
    price = models.IntegerField(verbose_name="Цена")
    url = models.CharField(max_length=255, verbose_name="Ссылка на канал")
    id_chanel = models.BigIntegerField(verbose_name="id канала", null=True, blank=True)
    user_friendly_id = models.BigIntegerField(
        verbose_name="Уникальный идентификатор(не менять, в случае удаления строки, добавить новую"
                     " с тем же id, или все сломается)",
        unique=True, null=True, blank=True,
    )

    class Meta:
        db_table = "pay_settings"
        verbose_name = "Настройка оплаты"
        verbose_name_plural = "Настройки оплаты"


class HelloMessage(models.Model):
    message = models.TextField(verbose_name="Приветственное сообщение")
    user_friendly_id = models.BigIntegerField(
        verbose_name="Уникальный идентификатор(не менять, в случае удаления строки, добавить новую"
                     " с тем же id, или все сломается)",
        unique=True, null=True, blank=True,
    )

    class Meta:
        db_table = "hello_message"
        verbose_name = "Приветственное сообщение"
        verbose_name_plural = "Приветственное сообщение"


class HelpChat(models.Model):
    message = models.TextField(verbose_name="Username чата")
    user_friendly_id = models.BigIntegerField(
        verbose_name="Уникальный идентификатор(не менять, в случае удаления строки, добавить новую"
                     " с тем же id, или все сломается)",
        unique=True, null=True, blank=True,
    )

    class Meta:
        db_table = "help_chat"
        verbose_name = "чат помощи"
        verbose_name_plural = "чаты помощи"
