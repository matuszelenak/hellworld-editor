import json
import os
import subprocess
import uuid
import datetime

from celery.task import Task
from django.core.files.base import ContentFile

from django.db import transaction

from hellworld import settings
from submit.models import Submit, SubmitScore


class ScoringTask(Task):
    abstract = True

    def compile(self, submit):
        raise NotImplementedError

    def get_base_execution_command(self, exec_path):
        raise NotImplementedError

    def evaluate(self, submit, exec_path):
        base_command = self.get_base_execution_command(exec_path)

        log = []

        inputs_path = os.path.join(settings.MEDIA_ROOT, 'tasks', str(submit.task.pk), 'inputs')
        outputs_path = os.path.join(settings.MEDIA_ROOT, 'tasks', str(submit.task.pk), 'outputs')
        for infile_path in os.listdir(inputs_path):
            data = open(os.path.join(inputs_path, infile_path), 'rb').read()
            outfile_path = os.path.join(outputs_path, os.path.splitext(infile_path)[0] + '.out')
            output_data = open(outfile_path, 'rb').read().rstrip('\n'.encode('utf8'))

            start = datetime.datetime.now()
            try:
                run_command = 'ulimit -v {mem} -n 0 && {base}'.format(
                    mem=10,
                    base=base_command
                )
                p = subprocess.check_output([run_command],
                                            input=data,
                                            stderr=subprocess.STDOUT,
                                            timeout=submit.task.time_limit / 1000,
                                            shell=True,
                                            executable='/bin/bash'
                                            )
            except subprocess.CalledProcessError:
                # Runtime exception
                log.append({
                    'input': infile_path,
                    'elapsed': int((datetime.datetime.now() - start).total_seconds() * 1000),
                    'status': 'EXC'
                })
                submit.status = Submit.STATUS_RUNTIME_EXCEPTION
                return log
            except subprocess.TimeoutExpired:
                # Time limit exceeded
                log.append({
                    'input': infile_path,
                    'elapsed': submit.task.time_limit,
                    'status': 'TLE'
                })
                submit.status = Submit.STATUS_TIME_LIMIT_EXCEEDED
                return log

            if p != output_data:
                # Wrong answer
                print(p)
                log.append({
                    'input': infile_path,
                    'elapsed': int((datetime.datetime.now() - start).total_seconds() * 1000),
                    'status': 'WA'
                })
                submit.status = Submit.STATUS_WA
                return log
            else:
                # OK
                log.append({
                    'input': infile_path,
                    'elapsed': int((datetime.datetime.now() - start).total_seconds() * 1000),
                    'status': 'OK'
                })
        submit.status = Submit.STATUS_OK
        return log

    @transaction.atomic
    def run(self, submit_pk, *args, **kwargs):
        submit = Submit.objects.select_for_update().get(pk=submit_pk)
        submit.status = Submit.STATUS_RUNNING

        compilation = self.compile(submit)
        log_dict = []
        if compilation['code'] != 0:
            submit.status = Submit.STATUS_COMPILATION_ERROR
        else:
            log_dict = self.evaluate(submit, compilation['exec_path'])

        score = SubmitScore.objects.create(
            compilation_message=compilation['compilation_message'],
            submit=submit,
            points=0
        )
        score.log_file.save('{}'.format(score.pk), ContentFile(json.dumps(log_dict)))
        score.save()

        submit.scoring_task_id = None
        submit.save()


class PythonScoringTask(ScoringTask):
    def compile(self, submit):
        return {
            'code': 0,
            'compilation_message': 'No compilation needed',
            'exec_path': os.path.join(settings.MEDIA_ROOT, submit.file.name)
        }

    def get_base_execution_command(self, exec_path):
        return 'python {}'.format(exec_path)


class CppScoringTask(ScoringTask):

    def compile(self, submit):
        in_file_path = os.path.join(settings.MEDIA_ROOT, submit.file.name)
        out_file_path = os.path.join(settings.COMPILED_BINARIES_PATH, str(uuid.uuid4()))

        try:
            subprocess.check_output(["g++", "-Wall", "-o", out_file_path, in_file_path], cwd=settings.MEDIA_ROOT, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            err_msg = e.output.decode('utf8')
            return {
                'code': e.returncode,
                'compilation_message': err_msg,
                'exec_path': None
            }

        return {
            'code': 0,
            'compilation_message': 'Compilation successful',
            'exec_path': out_file_path
        }

    def get_base_execution_command(self, exec_path):
        return str(exec_path)
