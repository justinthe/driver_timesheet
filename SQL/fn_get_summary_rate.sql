/*******************************************************************************

## get_summary_rate

Get a sumarized report of timesheet plus its calculation for a given period. 

Parameters:
- p_dtstart (date)      : period start
- p_dtend (date)        : period end
- p_userid (integer)    : userid

returns:
table:
dte (date) - date
hr_ot (double precision) - overtime duration in hour
holiday (boolean) - is holiday or not
timein (timestamp without timezone) - time check in
timeout (timestamp without timezone) - time check out
tot_allowance (double precision) - total allowance for selected period

usage:
select 
    * 
from 
    get_summary_rate('1/jan/2021', '15/jan/2021', 24)


Ver:
1.0     - 20210804    -   Initial version                       - JThe


 ********************************************************************************/

-- FUNCTION: public.get_summary_rate(date, date, integer)

-- DROP FUNCTION public.get_summary_rate(date, date, integer);

CREATE OR REPLACE FUNCTION public.get_summary_rate(
	p_dtstart date,
	p_dtend date,
	p_userid integer)
    RETURNS TABLE(dte date, hr_ot double precision, holiday boolean, timein timestamp without time zone, timeout timestamp without time zone, tot_allowance double precision) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
begin

create temp table if not exists ot_allowance as
select
	cast(parameter_value as double precision) as val
from
	rf_config
where
	parameter = 'ot_allowance'
	and dtstart = (select max(dtstart) from rf_config where parameter = 'ot_allowance');

create temp table if not exists daily_allowance as
select
	cast(parameter_value as double precision) as val
from
	rf_config
where
	parameter = 'daily_allowance'
	and dtstart = (select max(dtstart) from rf_config where parameter = 'daily_allowance');

create temp table if not exists ot_rate as
select
	cast(parameter_value as double precision) as val
from
	rf_config
where
	parameter = 'ot_hourly_rate'
	and dtstart = (select max(dtstart) from rf_config where parameter = 'ot_hourly_rate');

create temp table if not exists summary_n_rate as
select 
	gt.dte,
	gt.min_ot,
	gt.holiday,
	gt.timein,
	gt.timeout,
	ort.val as ot_rate,
	da.val as daily_allowance,
	oa.val as ot_allowance
from 
-- 	get_summary_timesheet('1/jan/2021', '17/jan/2021', 24) as gt
	get_summary_timesheet(p_dtstart, p_dtend, p_userid) as gt
cross join
	ot_rate as ort
cross join
	daily_allowance as da
cross join
	ot_allowance as oa;

return query
select
	x.dte,
	x.min_ot,
	x.holiday,
	x.timein,
	x.timeout,
-- 	x.ot_allowance,
	case when x.holiday is true then 0 else x.ot_allowance end + x.allowance as tot_allowance
from
	(
		select 
			sr.dte,
			sr.min_ot,
			sr.holiday,
			sr.timein,
			sr.timeout,
			case 
				when sr.holiday is true then sr.ot_allowance
				else sr.daily_allowance
			end as allowance,
			sr.min_ot * sr.ot_rate as ot_allowance
-- 			sr.ot_rate
-- 			sr.daily_allowance
-- 			sr.ot_allowance	
		from
			summary_n_rate sr
	) x;
end;
$BODY$;

ALTER FUNCTION public.get_summary_rate(date, date, integer)
    OWNER TO postgres;

