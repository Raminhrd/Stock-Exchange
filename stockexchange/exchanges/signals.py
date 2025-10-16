from django.dispatch import receiver
from django.db.models.signals import post_save
from exchanges.models import *


@receiver(post_save, sender=Order)
def check_price(sender, instance, created, **kwargs):