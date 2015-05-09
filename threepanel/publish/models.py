from django.db import models
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import timedelta

from slugify import slugify

from dashboard.models import SiteOptions

import random_name

# Create your models here.

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

    def send_mail(self, subject, message):
        siteoptions = SiteOptions.get()
        send_mail(subject=subject,
                  message=message,
                  from_email=siteoptions.email,
                  recipient_list=[self.email],
                  fail_silently=False)
        self.last_email_sent = timezone.now()
        self.save()

    def verify(self, request):
        siteoptions = SiteOptions.get()
        verify_url = request.build_absolute_uri(reverse('publish.views.verify',
                                                        kwargs={'email':self.email,
                                                                'verification_code':self.verification_code}))
        self.send_mail(subject="Welcome to {}!".format(siteoptions.title),
                       message=verify_url)

    @classmethod
    def tidy(cls):
        two_days_old = timezone.now() - timedelta(days=2)
        unverified = EmailSubscriber.objects.filter(verified=False,
                                                    created__lt=two_days_old)
        for subscriber in unverified:
            subscriber.delete()
