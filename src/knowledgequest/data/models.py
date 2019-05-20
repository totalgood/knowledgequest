from django.db import models


class User(models.Model):
    real_name = models.CharField(
        null=True, blank=True, max_length=255,
        help_text="""You can optionally provide your full name in order to help friends find you.
                     For each connection request you will be allowed to respond without revealing your real name, unless you choose to.
                  """)
    public_name = models.CharField(null=False, blank=True, max_length=32,
                                   help_text="This is the public username that others will see associated with your contributions.")
    reddit_username = models.CharField(null=True, blank=True, max_length=32)
    # email = models.EmailField(max_length=255)


class Email(models.Model):
    user = models.ForeignKey(
        User, null=False, blank=True,
        help_text="""You must have at least one verified email address associated with your account.
                     We never share any of your contact information with anyone.""")
