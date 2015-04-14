from django.db import models

# Create your models here.
class SiteOptions(models.Model):
    title = models.CharField(max_length=100, 
                             default="Super Cool Comic X",
                             help_text="The title of your comic")
    tagline = models.CharField(max_length=100,
                               default="A super cool comic about things!", 
                               help_text="A short tagline for your comic")
    elevator_pitch = models.TextField(default="",
                            help_text="A Tweet-length description of your comic.")
    mobile_logo_url = models.CharField(max_length=200,
                                default="http://butts.butts/butts.jpg",
                                help_text="The URL for the mobile-sized (width:300px, height:150px) logo to the website.")
    desktop_logo_url = models.CharField(max_length=200,
                                default="http://butts.butts/deskbutts.jpg",
                                help_text="The URL for the desktop-sized (width:500px, height:100px) logo to the website.")
    # Google tracking code number
    # Twitter 
    # DISQUS
   
    @classmethod
    def get(cls):
        opts = SiteOptions.objects.all()
        if len(opts) > 0:
            return opts[0]
        else:
            new_options = SiteOptions()
            new_options.save()
            return new_options
