/*******************************************************************************

## get_approved_timesheet

Get approved record of timesheet for a given period. 

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
    get_approved_timesheet('1/jan/2021', '15/jan/2021', 24)


Ver:
1.0     - 20210730    -   Initial version                       - JThe
1.1     - 20210802    -   Only showed approved timesheet        - JThe

 ********************************************************************************/


DROP FUNCTION IF EXISTS public.get_approved_timesheet(date, date, integer);

CREATE OR REPLACE FUNCTION public.get_approved_timesheet(
	p_dtstart date,
	p_dtend date,
	p_userid integer)
    RETURNS TABLE(dte date, timein timestamp without time zone, timeout timestamp without time zone) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
begin
        create temp table if not exists tmp_timesheet as
        select
            timesheetid,
            userid,
            dttimeenter,
            inout
        from
            timesheet
        where
            dttimeenter >= p_dtstart        -- '1/jan/2021'
            and dttimeenter <= p_dtend      -- '25/jan/2021'
            and userid = p_userid           -- 24
            and exists 
            (
                select 1
                from
                    approval
                where
                    approval.timesheetid = timesheet.timesheetid
                    and approval.approval is true
            );

		create temp table if not exists tmp_agg as
		select 
			inout, 
			date(dttimeenter) as dt,
			min(dttimeenter) as mindttimeenter,
			max(dttimeenter) as maxdttimeenter
		from 
			tmp_timesheet
		-- where
		-- 	dttimeenter >= p_dtstart		 	--'20/jul/2021'
		-- 	and dttimeenter <= p_dtend			--'25/jul/2021'
		-- 	and userid = p_userid				--23
		group by
			date(dttimeenter),
			inout;

		return query
		select
			coalesce(x.dt, y.dt) as dte, 
			-- date_part('minute', maxdttimeenter - mindttimeenter) as durminutes,
			mindttimeenter as timein,
			maxdttimeenter as timeout 
			
		from
			(
				select 
					dt, 
					mindttimeenter
				from 
					tmp_agg
				where
					inout = true
			) x
		join
			(
				select
					dt,
					maxdttimeenter
				from
					tmp_agg
				where
					inout = false
			) y
		on
			x.dt = y.dt;
	
end;
$BODY$;


