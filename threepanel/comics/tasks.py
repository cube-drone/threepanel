from __future__ import absolute_import

from django.core.mail import mail_admins

from celery import shared_task

from publish.models import EmailSubscriber, SpamSpamSpamSpam
from dashboard.models import SiteOptions

from comics.models import Comic, Blog

@shared_task
def publish():
    publog = []

    hero = Comic.hero()
    if hero.published:
        return

    print("Publishing!")
    publog.append("We're publishing a comic! Hooray!")
    publog.append(str(hero))
    hero.published = True
    hero.save()

    # send hero e-mail to subscribers
    subscribers = EmailSubscriber.subscribers()

    mails = []
    for subscriber in subscribers:
        try:
            print("Sending comic to {}".format(subscriber.email))
            publog.append("Sending comic to {}".format(subscriber.email))
            subscriber.send_promo_email(hero)
        except SpamSpamSpamSpam:
            print("\tCan't send: SPAM limit!")
            publog.append("\tCan't send: SPAM limit!")
        except Exception as e:
            raise e
            publog.append(e)

    # tweet hero tweet

    # send printed report to admin
    mail_admins(subject="Published!",
                message="\n".join(publog))

    mail_admins

    return

