import boto3
from StringIO import StringIO
import urllib
from zipfile import ZipFile

client = boto3.client('s3')
s3 = boto3.resource('s3')

BUCKET_NAME = 'FILL ME IN'

def lambda_handler(event, context):
    # TODO implement
    print event
    bucket = event['Records'][0]['s3']['bucket']['name']
    zip_key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    zipped = client.get_object(Bucket=bucket, Key=zip_key)
    in_mem_zip = StringIO(zipped.get('Body').read())
    input_zip=ZipFile(in_mem_zip)
    file_dict = {name: input_zip.read(name) for name in input_zip.namelist()}
    for file_name, file_body in file_dict.iteritems():
        object_name = zip_key.split('.')[0] + '/' + file_name
        s3.Object(BUCKET_NAME, object_name).put(Body=file_body)
    return 'Unzipped'