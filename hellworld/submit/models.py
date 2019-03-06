from django.db import models


class Submit(models.Model):
    LANGUAGE_CHOICES = (
        ('Python', 0),
        ('C/C++', 1)
    )
    participant_id = models.ForeignKey('people.Participant', related_name='submits', on_delete=models.CASCADE)
    content = models.TextField(null=False)
    language = models.IntegerField(choices=LANGUAGE_CHOICES, null=False)


class SubmitScore(models.Model):
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

    submit_id = models.ForeignKey('submit.Submit', related_name='scores', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, null=False)
    log_file = models.FileField(upload_to='scoring_logs')
    scoring_task_id = models.CharField(max_length=36, null=True)
