import json
import os
import subprocess
import uuid
import datetime
import shutil

import boto3
from celery.task import Task
from django.core.files.base import ContentFile

from django.db import transaction
from django.conf import settings

from submit.models import Submit, SubmitScore


class UpdateTaskInputs(Task):
    def run(self, *args, **kwargs):
        pks = kwargs['task_pks']

        client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        for pk in pks:
            response = client.list_objects(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Prefix=f'private/task_inputs/{pk}/'
            )

            shutil.rmtree(f'/{settings.INPUT_PATH}/{pk}/', ignore_errors=True)
            os.mkdir(f'/{settings.INPUT_PATH}/{pk}/')

            for file in response['Contents']:

                if not os.path.splitext(file['Key'])[1] in (settings.INPUTS_EXT, settings.OUTPUTS_EXT):
                    continue

                filename = file['Key'].rsplit('/')[-1]
                client.download_file(settings.AWS_STORAGE_BUCKET_NAME, file['Key'], f'/{settings.INPUT_PATH}/{pk}/{filename}')


class ScoringTask(Task):
    abstract = True

    def compile(self, submit):
        raise NotImplementedError

    def get_base_execution_command(self, exec_path):
        raise NotImplementedError

    def copy_code_to_local(self, submit, ext=''):
        filename = os.path.join(os.sep, 'tmp', str(uuid.uuid4()) + ext)
        with open(filename, 'wb') as f:
            submit.file.open('rb')
            f.write(submit.file.read())
            submit.file.close()
        return filename

    def evaluate(self, submit, exec_path):
        base_command = self.get_base_execution_command(exec_path)

        log = []
        points = 0

        inputs_path = os.path.join(os.sep, settings.INPUT_PATH, str(submit.task.pk))
        print(inputs_path)

        for infile_path in sorted([x for x in os.listdir(inputs_path) if os.path.splitext(x)[-1] == '.in']):
            input_data = open(os.path.join(inputs_path, infile_path), 'rb').read()
            output_data = open(os.path.join(inputs_path, os.path.splitext(infile_path)[0] + '.out'), 'rb').read()

            start = datetime.datetime.now()
            try:
                run_command = '{base}'.format(
                    base=base_command
                )
                print(run_command)
                p = subprocess.check_output([run_command],
                                            input=input_data,
                                            stderr=subprocess.STDOUT,
                                            timeout=submit.task.time_limit / 1000,
                                            shell=True,
                                            executable='/bin/bash'
                                            )
            except subprocess.CalledProcessError as err:
                # Runtime exception
                print(err)
                log.append({
                    'input': infile_path,
                    'elapsed': int((datetime.datetime.now() - start).total_seconds() * 1000),
                    'status': 'EXC'
                })
                submit.status = Submit.STATUS_RUNTIME_EXCEPTION
                return log, points
            except subprocess.TimeoutExpired:
                # Time limit exceeded
                log.append({
                    'input': infile_path,
                    'elapsed': submit.task.time_limit,
                    'status': 'TLE'
                })
                submit.status = Submit.STATUS_TIME_LIMIT_EXCEEDED
                return log, points

            if p != output_data:
                # Wrong answer
                print(output_data)
                print(p)
                log.append({
                    'input': infile_path,
                    'elapsed': int((datetime.datetime.now() - start).total_seconds() * 1000),
                    'status': 'WA'
                })
                submit.status = Submit.STATUS_WA
                return log, points
            else:
                # OK
                log.append({
                    'input': infile_path,
                    'elapsed': int((datetime.datetime.now() - start).total_seconds() * 1000),
                    'status': 'OK'
                })
                points += 1

        submit.status = Submit.STATUS_OK
        os.remove(exec_path)
        return log, points

    @transaction.atomic
    def run(self, submit_pk, *args, **kwargs):
        submit = Submit.objects.select_for_update().get(pk=submit_pk)
        submit.status = Submit.STATUS_RUNNING

        compilation = self.compile(submit)
        log_dict = []
        if compilation['code'] != 0:
            submit.status = Submit.STATUS_COMPILATION_ERROR
            points = 0
        else:
            log_dict, points = self.evaluate(submit, compilation['exec_path'])

        score = SubmitScore.objects.create(
            compilation_message=compilation['compilation_message'],
            submit=submit,
            points=points
        )
        score.log_file.save('{}'.format(score.pk), ContentFile(json.dumps(log_dict).encode('utf-8')))
        score.save()

        submit.scoring_task_id = None
        submit.save()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super().on_failure(exc, task_id, args, kwargs, einfo)
        Submit.objects.filter(pk=kwargs['submit_pk']).update(status=Submit.STATUS_SCORING_FAILED)


class PythonScoringTask(ScoringTask):
    def compile(self, submit):
        return {
            'code': 0,
            'compilation_message': 'No compilation needed',
            'exec_path': self.copy_code_to_local(submit, ext='.py')
        }

    def get_base_execution_command(self, exec_path):
        return 'python {}'.format(exec_path)


class CppScoringTask(ScoringTask):

    def compile(self, submit):
        in_file_path = self.copy_code_to_local(submit, ext='.cpp')
        out_file_path = os.path.join(os.sep, 'tmp', str(uuid.uuid4()))

        try:
            subprocess.check_output(["g++", "-Wall", "-o", out_file_path, in_file_path], cwd=settings.MEDIA_ROOT, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            err_msg = e.output.decode('utf8')
            print(err_msg)
            return {
                'code': e.returncode,
                'compilation_message': err_msg,
                'exec_path': None
            }
        finally:
            os.remove(in_file_path)

        return {
            'code': 0,
            'compilation_message': 'Compilation successful',
            'exec_path': out_file_path
        }

    def get_base_execution_command(self, exec_path):
        return str(exec_path)
