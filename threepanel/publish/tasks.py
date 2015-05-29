from __future__ import absolute_import

from django.core.mail import mail_admins

from celery import shared_task

from publish.models import EmailSubscriber

from comics.models import Comic, Blog

@shared_task
def tidy_subscribers():
    deleted_subscribers = []
    for subscriber in EmailSubscriber.tidy():
        deleted_subscribers.append(subscriber.email)

    if len(deleted_subscribers) > 0:
        mail_admins(subject="These unverified subscribers deleted:",
                    message="\n".join(deleted_subscribers))

