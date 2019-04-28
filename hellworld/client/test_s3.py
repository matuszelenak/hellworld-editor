import os
import shutil

import boto3

AWS_ACCESS_KEY_ID = 'AKIAZL4EH7Q3YL7BQNGP'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'hellworld-editor'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = None

client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

response = client.list_objects(
    Bucket=AWS_STORAGE_BUCKET_NAME,
    Prefix='private/task_inputs/3/'
)

# Loop through each file
for file in response['Contents']:
    if not os.path.splitext(file['Key'])[1] in ('.in', '.out'):
        continue

    print(file['Key'])

    client.download_file(AWS_STORAGE_BUCKET_NAME, file['Key'], file['Key'].rsplit('/')[-1])
