# vim: ts=2:sw=2:expandtab:softtabstop=2
import boto3, sys, os#, json
import urllib.request


#======================================================================
def check_ssh_keys():
 print("===")
 try:
    response = urllib.request.urlopen('http://checkip.amazonaws.com/')
    # Could use https://api.myip.com
    #r1 = json.loads(response.read())
    r1 = response.read()
    extip = r1#['ip']
    # TODO: Do I want to add this IP to the "default" secgroup here?
    # Not sure, it might be many groups and I wouldn't want to play there.
    open(f"{homedir}/oracle.pem")
 except Exception as e:
    print('\n========================================')
    print('Before using this demo, you need to:')
    print('- copy this account\'s SSH private key to file ~/oracle.pem')
    print(f'- add your external IP {extip} to this account\'s '
       'security group to allow all traffic')
    print('Exiting now. Restart this script when all requirements are met.')
    print('========================================\n')
    # print(e)
    sys.exit(1)

#======================================================================
def first_connect(privip, pubip):
 # ssh -o "StrictHostKeyChecking no" -i ~/oracle.pem oracle@3.14.82.108
 # /opt/oracle/product/19c/dbhome_1/network/admin/listener.ora 
 newlisttext = f"""

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = {privip})(PORT = 1521))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )

"""
 newtnstext = f"""

ORCLCDB =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = {privip})(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = ORCLCDB)
    )
  )

LISTENER =
  (ADDRESS = (PROTOCOL = TCP)(HOST = {privip})(PORT = 1521))

"""

 orascript = """
ORACLE_SID=ORCLCDB
ORACLE_BASE=/opt/oracle
ORACLE_HOME=/opt/oracle/product/19c/dbhome_1
/opt/oracle/product/19c/dbhome_1/bin/lsnrctl start
/opt/oracle/product/19c/dbhome_1/bin/sqlplus -S /nolog <<EOT
conn / as sysdba
set feed off echo off time off head off timing off
startup
alter system set local_listener=LISTENER scope=both;
alter pluggable database all open;
alter system register;
conn dd/dd@//oul/ddpdb
show user con_id con_name
exit
EOT
"""

 try:
  f = open('/tmp/listener.ora', 'w')
  f.write(newlisttext)
  f.close()
  f = open('/tmp/tnsnames.ora', 'w')
  f.write(newtnstext)
  f.close()
  f = open('/tmp/s.sh', 'w')
  f.write(orascript)
  f.close()

  cmd=(
   "ssh -o \"StrictHostKeyChecking no\""
   f" -i ~/oracle.pem oracle@{pubip} uname -a "
  )
  #print(cmd)
  os.system(cmd)

  cmd=(
   f"scp -i {homedir}/oracle.pem /tmp/listener.ora"
   f"  oracle@{pubip}:/opt/oracle/product/19c/dbhome_1/network/admin/listener.ora"
  )
  #print(cmd)
  os.system(cmd)

  cmd=(
   f"scp -i {homedir}/oracle.pem /tmp/tnsnames.ora"
   f"  oracle@{pubip}:/opt/oracle/product/19c/dbhome_1/network/admin/tnsnames.ora"
  )
  #print(cmd)
  os.system(cmd)

  cmd=(
   f"scp -i {homedir}/oracle.pem /tmp/s.sh"
   f"  oracle@{pubip}:/home/oracle/s.sh"
  )
  #print(cmd)
  os.system(cmd)

  cmd=(
   f"ssh -i ~/oracle.pem oracle@{pubip} bash /home/oracle/s.sh"
  )
  #print(cmd)
  os.system(cmd)

 except Exception as e:
  print('\n========================================')
  print('Before using this demo, you need to:')
  print('- copy this account\'s SSH private key to file ~/oracle.pem')
  print(f'- add your external IP {extip} to this account\'s '
   'security group to allow all traffic')
  print('Exiting now. Restart this script when all requirements are met.')
  print('========================================\n')
  print(e)
  sys.exit(1)


#======================================================================
# Init
homedir = os.path.expanduser("~")
check_ssh_keys()
