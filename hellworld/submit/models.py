from django.db import models


class Task(models.Model):
    name = models.TextField(null=False)
    assignment_text = models.TextField(null=False)
    input_path = models.TextField(null=False)
    max_points = models.IntegerField(null=False)


class Submit(models.Model):
    STATUS_WAITING = 0
    STATUS_RUNNING = 1
    STATUS_OK = 2
    STATUS_WA = 3
    STATUS_COMPILATION_ERROR = 4
    STATUS_SEGFAULT = 5
    STATUS_RUNTIME_EXCEPTION = 6

    STATUS_CHOICES = (
        ('Waiting', STATUS_WAITING),
        ('Running', STATUS_RUNNING),
        ('OK', STATUS_OK),
        ('WA', STATUS_WA),
        ('Compilation error', STATUS_COMPILATION_ERROR),
        ('Segmentation fault', STATUS_SEGFAULT),
        ('Runtime exception', STATUS_RUNTIME_EXCEPTION)
    )

    LANGUAGE_PYTHON = 0
    LANGUAGE_CPP = 1

    LANGUAGE_CHOICES = (
        ('Python', LANGUAGE_PYTHON),
        ('C/C++', LANGUAGE_CPP)
    )
    participant = models.ForeignKey('people.Participant', related_name='submits', on_delete=models.CASCADE, null=True)
    task = models.ForeignKey('submit.Task', related_name='submits', on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='submits')
    language = models.IntegerField(choices=LANGUAGE_CHOICES, null=False)

    scoring_task_id = models.CharField(max_length=36, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, null=False, default=STATUS_WAITING)

    def run_scoring(self):
        from .tasks import PythonScoringTask, CppScoringTask
        if self.language == self.LANGUAGE_PYTHON:
            scoring_task_cls = PythonScoringTask
        else:
            scoring_task_cls = CppScoringTask

        self.status = self.STATUS_WAITING
        self.scoring_task_id = scoring_task_cls().delay(self.pk).task_id


class SubmitScore(models.Model):

    submit = models.ForeignKey('submit.Submit', related_name='scores', on_delete=models.CASCADE)
    log_file = models.FileField(upload_to='scoring_logs')
    points = models.IntegerField(default=0)
