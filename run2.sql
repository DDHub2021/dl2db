conn dd/dd@//oul/ddpdb
/*
USE YOUR AWS Credentials to access YOUR S3 from Oracle process.
(from ~/.aws/credentials)
*/
begin
  DBMS_CLOUD.CREATE_CREDENTIAL (
      'ddoracle',
      'DEADBEEFDEADBEEF',
      'DEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEF');
end;
/
commit;
select * from dba_credentials;

/*
Accessing "live" data in S3, without copying it into Oracle DB
USE YOUR AWS S3 bucket name.
https://docs.oracle.com/en/cloud/paas/autonomous-database/adbdu/
 format-parameter.html#GUID-C9B6551F-C135-455A-B671-AE791C15A194
*/
BEGIN
    DBMS_CLOUD.CREATE_EXTERNAL_TABLE(
     table_name =>'EXT_NYC_CABS',
     credential_name =>'DDORACLE',
     file_uri_list =>'https://s3-aidayc2q6y2eflhctx7wh.s3.us-east-2.amazonaws.com/yellow_tripdata_2020-01.csv',
     column_list =>    'VENDOR_ID NUMBER,
                        PICKUP_DATE DATE,
                        DROPOFF_DATE DATE,
                        PASSENGERS NUMBER,
                        MILES_TRAVELLED NUMBER,
                        RATECODE_ID NUMBER,
                        STORE_FWD_FLAG CHAR(1),
                        PULOC_ID NUMBER,
                        DOLOC_ID NUMBER,
                        PAY_TYPE NUMBER,
                        FARE_AMNT NUMBER,
                        EXTRA_AMNT NUMBER,
                        MTA_TAX NUMBER,
                        TIP NUMBER,
                        TOLLS NUMBER,
                        IMPRV_SURCH NUMBER,
                        TOTAL_AMNT NUMBER,
                        CONG_SURCH NUMBER
                        ',
     format => json_object(
      'dateformat' value 'YYYY-MM-DD HH24:MI:SS',
      'ignoremissingcolumns' value 'true', 
      'removequotes' value 'false',
      'ignoreblanklines' value 'true',
      'skipheaders' value '1',
      'trimspaces' value 'lrtrim',
      'truncatecol' value 'true',
      'type' value 'csv'
    )
  );
 END;
 /
commit; -- This one _is_ important!

/* This will take a long time.
   Must respond: "PL/SQL procedure successfully completed."
*/
EXECUTE DBMS_CLOUD.VALIDATE_EXTERNAL_TABLE ('EXT_NYC_CABS')
/


