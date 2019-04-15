import time

from django.core.management.base import BaseCommand
from django.db import transaction

from submit.models import Submit


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        for s in Submit.objects.filter(status=Submit.STATUS_WAITING):
            s.run_scoring()
            time.sleep(10)
