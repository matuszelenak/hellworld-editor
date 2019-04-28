import os

from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


from submit.models import Task


@receiver(post_save, sender=Task)
def generate_test_folders(sender, instance, *args, **kwargs):
    if kwargs['created']:
        os.mkdir(os.path.join(settings.TASK_ROOT, str(instance.pk)))
