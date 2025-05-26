import io
import threading

import requests

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InputText, BinaryDocument, Client
from adminka.settings import BOT_TOKEN


@receiver(post_save, sender=InputText)
def mymodel_created_handler(sender, instance, created, **kwargs):
    if created:
        threading.Thread(target=spam, args=(instance.text_input,)).start()


def spam(text):
    tg_url_doc = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'
    tg_url_message = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    all_spam_doc = list(BinaryDocument.objects.filter(status_file="RASS").all())
    all_clients = list(Client.objects.filter().all())
    for client in all_clients:
        if all_spam_doc:
            for doc in all_spam_doc:
                file_name = f"{doc.name}.{doc.expansion}"
                file_like = io.BytesIO(doc.file_data)
                file_like.name = file_name
                try:
                    result = requests.post(
                        url=tg_url_doc,
                        data={'chat_id': client.id, "caption": text},
                        files={'document': (file_name, file_like)}
                    )
                    print(result)
                except Exception as e:
                    print(e)
        else:
            payload = {
                'chat_id': client.id,
                'text': text,
                'parse_mode': 'HTML'
            }
            response = requests.post(tg_url_message, data=payload)
            print(response)
