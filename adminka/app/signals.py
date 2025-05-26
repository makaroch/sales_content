import io

import requests

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InputText, BinaryDocument, Client
from adminka.settings import BOT_TOKEN


@receiver(post_save, sender=InputText)
def mymodel_created_handler(sender, instance, created, **kwargs):
    if created:
        tg_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'
        all_spam_doc = list(BinaryDocument.objects.filter(status_file="RASS").all())
        all_clients = list(Client.objects.filter().all())
        text = instance.text_input
        for client in all_clients:
            for doc in all_spam_doc:
                file_name = f"{doc.name}.{doc.expansion}"
                file_like = io.BytesIO(doc.file_data)
                file_like.name = file_name
                try:
                    requests.post(
                        url=tg_url,
                        data={'chat_id': client.id, "caption": text},
                        files={'document': (file_name, file_like)}
                    )
                except Exception as e:
                    print(e)
