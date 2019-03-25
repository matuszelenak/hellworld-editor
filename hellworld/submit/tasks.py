import json

from celery.task import Task

from django.db import transaction

from submit.models import Submit, SubmitScore


class ScoringTask(Task):
    abstract = True

    def score_submit(self, submit):
        raise NotImplementedError

    @transaction.atomic
    def run(self, submit_pk, *args, **kwargs):
        submit = Submit.objects.get(pk=submit_pk)
        submit.status = Submit.STATUS_RUNNING

        points, log_dict = self.score_submit(submit)

        SubmitScore.objects.create(
            submit=submit,
            points=points,
            log_file=json.dumps(log_dict)
        )


class PythonScoringTask(ScoringTask):
    pass


class CppScoringTask(ScoringTask):
    pass
