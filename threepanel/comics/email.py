
COMIC_EMAIL = """
{promo_text}

The comic is available at:
{comic_absolute_url}

----
{alt_text}

"""

COMIC_EMAIL_HTML = """

<p>{promo_text}</p>

<a href='{comic_absolute_url}'>
    <img src='{image_url}' alt_text='{alt_text}' title='{secret_text}'></img>
</a>

<p>{secret_text}</p>

"""
