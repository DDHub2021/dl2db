# vim: ts=2:sw=2:expandtab:softtabstop=2
import boto3, sys, time

amiid = 'ami-0e1c04b7f2864a236'

def create_oracle_linux_instance(innm, rn):
   client = boto3.client("ec2", region_name=rn)
# Checking first
   descinsts = client.describe_instances(Filters=[
   {'Name':'image-id', 'Values': [amiid]},
   {'Name':'instance-state-name', 'Values': ['running']}
   ])
   if len(descinsts['Reservations']):
    pubip = descinsts['Reservations'][0]["Instances"][0]['PublicIpAddress'] 
    print(f'... the AMI {amiid} was already deployed with IP {pubip}') 
    instances = descinsts 
    return(instances, descinsts, pubip)
# Need to deploy new VM
   print(f'... deploying AMI {amiid}, please wait ...')
   try:
    instances = client.run_instances(
        ImageId=amiid,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
         {
          'ResourceType': 'instance',
          'Tags': [{ 'Key': 'Name', 'Value': innm }]
         }],
        InstanceType="r5.large"
#        , DryRun=True
#        , KeyName="ec2-key-pair" # We use ~/oracle.pem
    )
    print(f"... ({time.asctime()}) waiting 2 min before contacting {innm} on {rn}")
    time.sleep(120)
    inid = instances["Instances"][0]['InstanceId']
#    inid='i-05d0c2e8e900fe3fb' # DEBUG
    # Getting Public IP now
    descinsts = client.describe_instances(InstanceIds=[inid]) 
    #print(descinsts,"\n\n")
    pubip = descinsts['Reservations'][0]["Instances"][0]['PublicIpAddress']
    #print(pubip)
    instances = descinsts # DEBUG
    return(instances, descinsts, pubip)
   except Exception as e:
    print(e)
    sys.exit(1)
