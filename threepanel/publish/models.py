from datetime import timedelta

from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from slugify import slugify

from django.core.urlresolvers import reverse

from dashboard.models import SiteOptions
from comics.email import COMIC_EMAIL, COMIC_EMAIL_HTML
import random_name

from .email import VERIFICATION_EMAIL, VERIFICATION_EMAIL_HTML

class SpamSpamSpamSpam(Exception):
    """
    Thrown when you try to email the EmailSubscriber more than once a day.
    """
    pass

class EmailSubscriber(models.Model):
    """
    One e-mail, subscribed to your comic.
    """
    email = models.CharField(max_length=100, null=False, blank=False, unique=True)
    verification_code = models.CharField(max_length=200, null=False, blank=False)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField()
    last_email_sent = models.DateTimeField()

    def save(self):
        if not self.id:
            self.created = timezone.now()
            self.last_email_sent = timezone.now()
        if not self.verification_code:
            self.verification_code = slugify(random_name.special_thing())
        super().save()

    def send_verification_email(self):
        site_options = SiteOptions.get()

        site_url = settings.SITE_URL
        verification_relative_url = reverse('publish.views.verify',
                                            kwargs={'email':self.email,
                                                    'verification_code':self.verification_code})
        verification_absolute_url = "{}{}".format(site_url, verification_relative_url)

        subject = "Welcome to {}!".format(site_options.title)
        message = VERIFICATION_EMAIL.format(verification_absolute_url)
        messsage_html = VERIFICATION_EMAIL_HTML.format(verification_absolute_url)
        self.send_mail(subject, message, message_html)

    def send_promo_email(self, comic):
        site_options = SiteOptions.get()

        site_url = settings.SITE_URL
        comic_relative_url = reverse('comics.views.single',
                                     kwargs={'comic_slug':comic.slug})
        comic_absolute_url = "{}{}".format(site_url, comic_relative_url)

        subject = "{} - {}".format(site_options.title, comic.title)
        message = COMIC_EMAIL.format(promo_text=comic.promo_text,
                                     alt_text=comic.alt_text,
                                     comic_absolute_url=comic_absolute_url)
        message_html = COMIC_EMAIL_HTML.format(promo_text=comic.promo_text,
                                     alt_text=comic.alt_text,
                                     secret_text=comic.secret_text,
                                     image_url=comic.image_url,
                                     comic_absolute_url=comic_absolute_url)
        self.send_mail(subject, message, message_html)

    def send_mail(self, subject, message, html_message=None):
        one_day_ago = timezone.now() - timedelta(hours=23)
        if self.last_email_sent > one_day_ago:
            raise SpamSpamSpamSpam("You're sending e-mail too often.")

        site_options = SiteOptions.get()

        site_url = settings.SITE_URL
        unsubscribe_relative_url = reverse('publish.views.unsubscribe_email',
                                           kwargs={'email':self.email})
        unsubscribe_absolute_url = "{}{}".format(site_url, unsubscribe_relative_url)

        message = message + "\nTo unsubscribe forever from these messages, go to {}".format(unsubscribe_absolute_url)
        if html_message:
            html_message = html_message + """
<p>To unsubscribe forever from these messages, go to <a href='{}'>Unsubscribe</a>
            """.format(unsubscribe_absolute_url)

        self.last_email_sent = timezone.now()
        self.save()
        send_mail(subject=subject,
                  message=message,
                  from_email=settings.SERVER_EMAIL,
                  recipient_list=[self.email],
                  html_message=html_message,
                  fail_silently=False)

    def __str__(self):
        return "<Subscriber: {}>".format(self.email)

    @classmethod
    def tidy(cls):
        two_days_old = timezone.now() - timedelta(days=2)
        unverified = EmailSubscriber.objects.filter(verified=False,
                                                    created__lt=two_days_old)
        for subscriber in unverified:
            subscriber.delete()

    @classmethod
    def subscribers(cls):
        return EmailSubscriber.objects.filter(verified=True)
