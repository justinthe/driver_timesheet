/*

userid, date, durminutes_ot, durminutes, publicholiday
23, 22/jul/2021, 10, 350, false
23, 23/jul/2021, 0, 300, false
23, 24/jul/2021, 0, 300, true
23, 26/jul/2021, 50, 250, false


--> records only day driver presence

*/

with tmp_raw as (
select
	dte,
	to_timestamp(cast(dte as text) || ' 08:00:00', 'YYYY-MM-DD HH24:MI:SS') as tstart,
	to_timestamp(cast(dte as text) || ' 17:00:00', 'YYYY-MM-DD HH24:MI:SS') as tend,
	timein,
	timeout
from
	get_approved_timesheet('1/jan/2021', '15/jan/2021', 24)
)

, pub_holiday as (
select
	dt
from
	rf_special_day
where
	dt between '1/jan/2021' and '15/jan/2021'
	
)

select
	dte,
-- 	dy,
	((hr_morning_ot * 60) + (min_morning_ot) + (hr_evening_ot * 60) + (min_evening_ot))/60.0 as min_ot,
	pub_holiday,
	timein,
	timeout
from	
	(
		select
			dte,
			dy,
			case when hr_morning_ot <=0 then 0 else hr_morning_ot end as hr_morning_ot,
			case when min_morning_ot <=0 then 0 else min_morning_ot end as min_morning_ot,
			case when hr_evening_ot <=0 then 0 else hr_evening_ot end as hr_evening_ot,			
			case when min_evening_ot <=0 then 0 else min_evening_ot end as min_evening_ot,
			case 
				when dy = 0 then true
				when dt is not null then true
				else false end as pub_holiday,
			timein,
			timeout
		from
			(
				select 
					dt,
					dte, 
					extract(dow from dte) as dy,
-- 					age(tstart, timein) as morning_ot,
-- 					age(timeout, tend) as evening_ot,
					date_part('hour', tstart - timein) as hr_morning_ot,
					date_part('hour', timeout - tend) as hr_evening_ot,
					date_part('minute', tstart - timein) as min_morning_ot,
					date_part('minute', timeout - tend) as min_evening_ot,
					timein,
					timeout
				from
					tmp_raw
				left join
					pub_holiday 
				on
					dte = dt
			) x
	) y