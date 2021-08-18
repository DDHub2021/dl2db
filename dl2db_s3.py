# vim: ts=2:sw=2:expandtab:softtabstop=2
import boto3, sys
from botocore.client import ClientError

client = boto3.client('s3')

def create_s3(bn):
 try:
  rn = client.meta.region_name
  location = {'LocationConstraint': rn}
  bucket = client.create_bucket(Bucket=bn, CreateBucketConfiguration=location)
  return (rn, bucket)
 except ClientError as e:
   if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
    return (rn, False)
   else:
    print(e)
    sys.exit(1)

def put_s3(bn, fn):
 try:
  print(f'... storing file {fn}, please wait ...')
  client.put_object( Body=open(fn,'rb'),
   Bucket=bn, Key=fn)
 except ClientError as e:
   print(e)
   sys.exit(1)
