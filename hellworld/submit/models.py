from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=100, null=False)
    assignment = models.FileField(upload_to='tasks', null=True)
    max_points = models.IntegerField(null=False)
    time_limit = models.IntegerField(default=5000)
    memory_limit = models.IntegerField(default=5000)

    def __str__(self):
        return self.name


class Submit(models.Model):
    STATUS_WAITING = 0
    STATUS_RUNNING = 1
    STATUS_OK = 2
    STATUS_WA = 3
    STATUS_COMPILATION_ERROR = 4
    STATUS_RUNTIME_EXCEPTION = 5
    STATUS_TIME_LIMIT_EXCEEDED = 6

    STATUS_CHOICES = (
        (STATUS_WAITING, 'Waiting'),
        (STATUS_RUNNING, 'Running'),
        (STATUS_OK, 'OK'),
        (STATUS_WA, 'WA'),
        (STATUS_COMPILATION_ERROR, 'Compilation error'),
        (STATUS_RUNTIME_EXCEPTION, 'Runtime exception'),
        (STATUS_TIME_LIMIT_EXCEEDED, 'Time limit exceeded')
    )

    LANGUAGE_PYTHON = 0
    LANGUAGE_CPP = 1

    LANGUAGE_CHOICES = (
        (LANGUAGE_PYTHON, 'Python'),
        (LANGUAGE_CPP, 'C/C++')
    )

    LANGUAGE_EXTENSIONS = {
        LANGUAGE_PYTHON: '.py',
        LANGUAGE_CPP: '.cpp'
    }

    participant = models.ForeignKey('people.Participant', related_name='submits', on_delete=models.CASCADE, null=True)
    task = models.ForeignKey('submit.Task', related_name='submits', on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='submits')
    language = models.IntegerField(choices=LANGUAGE_CHOICES, null=False)

    scoring_task_id = models.CharField(max_length=36, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, null=False, default=STATUS_WAITING)

    def run_scoring(self):
        from .tasks import PythonScoringTask, CppScoringTask
        if self.language == self.LANGUAGE_PYTHON:
            scoring_task_cls = PythonScoringTask
        else:
            scoring_task_cls = CppScoringTask

        self.status = self.STATUS_WAITING
        self.scoring_task_id = scoring_task_cls().delay(self.pk).task_id
        self.save()


class SubmitScore(models.Model):

    submit = models.ForeignKey('submit.Submit', related_name='scores', on_delete=models.CASCADE)
    compilation_message = models.TextField()
    log_file = models.FileField(upload_to='scoring_logs')
    points = models.IntegerField(default=0)
    date_scored = models.DateTimeField(auto_now_add=True)
