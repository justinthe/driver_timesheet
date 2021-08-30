/*******************************************************************************

## get_summary_timesheet

Get a sumarized report of timesheet for a given period. 

Parameters:
- p_dtstart (date)      : period start
- p_dtend (date)        : period end
- p_userid (integer)    : userid

returns:
table:
dte (date) 
timein (timestamp without timezone)
timeout (timestamp without timezone)

usage:
select 
    * 
from 
    get_summary_timesheet('1/jan/2021', '15/jan/2021', 24)


Ver:
1.0     - 20210803    -   Initial version                       - JThe


 ********************************************************************************/
 
-- FUNCTION: public.get_summary_timesheet(date, date, integer)

-- DROP FUNCTION public.get_summary_timesheet(date, date, integer);

 
CREATE OR REPLACE FUNCTION public.get_summary_timesheet(
    p_dtstart date,
    p_dtend date,
    p_userid integer)
    RETURNS TABLE(dte date, min_ot double precision, holiday boolean, timein timestamp without time zone, timeout timestamp without time zone) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
begin

        create temp table if not exists tmp_raw as 
        select
            gat.dte,
            to_timestamp(cast(gat.dte as text) || ' 08:00:00', 'YYYY-MM-DD HH24:MI:SS') as tstart,
            to_timestamp(cast(gat.dte as text) || ' 17:00:00', 'YYYY-MM-DD HH24:MI:SS') as tend,
            gat.timein,
            gat.timeout
        from
--          get_approved_timesheet('1/jan/2021', '15/jan/2021', 24);
            get_approved_timesheet(p_dtstart, p_dtend, p_userid) as gat;
        
        create temp table if not exists pub_holiday as  
        select
            sd.dte
        from
            rf_special_day as sd
        where
--          dte between '1/jan/2021' and '15/jan/2021';
            sd.dte between p_dtstart and p_dtend;

        
        return query
        select
            y.dte as dte,
            ((y.hr_morning_ot * 60) + (y.min_morning_ot) + (y.hr_evening_ot * 60) + (y.min_evening_ot))/60.0 as min_ot,
            y.holiday,
            y.timein as timein,
            y.timeout as timeout
        from    
            (
                select
                    x.dte,
                    x.dy,
                    case when x.hr_morning_ot <=0 then 0 else x.hr_morning_ot end as hr_morning_ot,
                    case when x.min_morning_ot <=0 then 0 else x.min_morning_ot end as min_morning_ot,
                    case when x.hr_evening_ot <=0 then 0 else x.hr_evening_ot end as hr_evening_ot,         
                    case when x.min_evening_ot <=0 then 0 else x.min_evening_ot end as min_evening_ot,
                    case 
                        when x.dy = 0 then true
                        when x.dt is not null then true
                        else false end as holiday,
                    x.timein,
                    x.timeout
                from
                    (
                        select 
                            ph.dte as dt,
                            tr.dte as dte, 
                            extract(dow from tr.dte) as dy,
                            date_part('hour', tr.tstart - tr.timein) as hr_morning_ot,
                            date_part('hour', tr.timeout - tr.tend) as hr_evening_ot,
                            date_part('minute', tr.tstart - tr.timein) as min_morning_ot,
                            date_part('minute', tr.timeout - tr.tend) as min_evening_ot,
                            tr.timein,
                            tr.timeout
                        from
                            tmp_raw as tr
                        left join
                            pub_holiday as ph
                        on
                            tr.dte = ph.dte
                    ) x
            ) y
        order by
            y.dte;
    end;
$BODY$;

ALTER FUNCTION public.get_summary_timesheet(date, date, integer)
    OWNER TO postgres;
