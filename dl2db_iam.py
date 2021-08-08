# vim: ts=2:sw=2:expandtab:softtabstop=2
import boto3, sys

iam = boto3.resource('iam')

def get_current_user_id():
 try:
  current_user = iam.CurrentUser()
  return current_user.user_id.lower()
 except Exception as e:
  print(e)
  sys.exit(1)
