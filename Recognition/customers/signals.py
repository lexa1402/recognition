import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from customers.models import PageScan


@receiver(pre_delete, sender=PageScan)
def page_pre_delete(sender, instance, **kwargs):
    os.remove(instance.image.path)
