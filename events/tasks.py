from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .partials import mail


@shared_task(name="send_review_email_task")
def send_review_email_task(email, title):
    return mail.send_mail(email, title)
