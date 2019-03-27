import json

from celery.task import Task
from django.core.files.base import ContentFile

from django.db import transaction

from submit.models import Submit, SubmitScore


class ScoringTask(Task):
    abstract = True

    def score_submit(self, submit):
        raise NotImplementedError

    @transaction.atomic
    def run(self, submit_pk, *args, **kwargs):
        submit = Submit.objects.select_for_update().get(pk=submit_pk)
        submit.status = Submit.STATUS_RUNNING

        points, log_dict = self.score_submit(submit)

        score = SubmitScore.objects.create(
            submit=submit,
            points=points
        )
        score.log_file.save('{}'.format(score.pk), ContentFile(json.dumps(log_dict)))
        score.save()

        submit.scoring_task_id = None
        submit.save()


class PythonScoringTask(ScoringTask):
    def score_submit(self, submit):
        submit.status = Submit.STATUS_OK
        return 1, []


class CppScoringTask(ScoringTask):
    def score_submit(self, submit):
        submit.status = Submit.STATUS_OK
        return 1, []
