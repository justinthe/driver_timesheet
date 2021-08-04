--https://stackoverflow.com/questions/1490942/how-to-declare-a-variable-in-a-postgresql-query

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
	get_summary_timesheet('1/jan/2021', '17/jan/2021', 24) as gt
cross join
	ot_rate as ort
cross join
	daily_allowance as da
cross join
	ot_allowance as oa;
	
select
	x.dte,
	x.min_ot as hr_ot, 
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