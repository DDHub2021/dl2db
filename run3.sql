conn dd/dd@//oul/ddpdb

select * from EXT_NYC_CABS fetch first 5 rows only;

with enc as (
select avg(TOTAL_AMNT) avgtotal, avg(TIP) avgtip
from EXT_NYC_CABS)
select round(enc.avgtip/enc.avgtotal,2)*100 tip_pct
from enc
/

select /*+ PARALLEL(EXT_NYC_CABS 6) */ PULOC_ID, DOLOC_ID, count(*) TRIPS
from EXT_NYC_CABS
group by PULOC_ID, DOLOC_ID
order by TRIPS desc
fetch first 5 rows only
/

explain plan for
select /*+ PARALLEL(EXT_NYC_CABS 6) */ PULOC_ID, DOLOC_ID, count(*) TRIPS
from EXT_NYC_CABS
group by PULOC_ID, DOLOC_ID
order by TRIPS desc
fetch first 5 rows only
/

set lines 150
select * from dbms_xplan.display();
