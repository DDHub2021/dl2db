#!/usr/bin/env python3
# vim: ts=2:sw=2:expandtab:softtabstop=2
from dl2db_ssh import *
from dl2db_iam import *
from dl2db_s3 import *
from dl2db_ec2 import *

NYCCabFile = 'yellow_tripdata_2020-01.csv'

# All "global" things, like S3 bucket name, will be linked to this user ID
cur_uid = get_current_user_id()
s3name = f"s3-{cur_uid}"
ec2name = f"oul-{cur_uid}"
print(f"... running as user {cur_uid}")
(region, s3bt) = create_s3(s3name)
print(f"... using S3 bucket {s3name} in {region}")
print("... Full 566MB data set: https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2020-01.csv")
print("... You can download it and overwrite this short version.")
put_s3(s3name, NYCCabFile)
print(f"... launching OUL VM {ec2name} in {region}")
(ec2i, ec2inst, ec2pubip)  = create_oracle_linux_instance(ec2name, region)
# Described instance is "ec2inst". The "ec2i" is returned by deployment call.
ec2privip = ec2inst['Reservations'][0]["Instances"][0]['PrivateIpAddress']
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/ \
#  services/ec2.html#EC2.Client.run_instances
print(f"... launched Instance {ec2name} ({ec2pubip}) in {region}")
# Starting "ssh ping-pong" with Oracle
first_connect(ec2privip, ec2pubip)
print(f"=== End. Connect with SQL tool to {ec2name} ({ec2pubip}) "
 f"in {region} and run SQL scripts in sequential order.")
