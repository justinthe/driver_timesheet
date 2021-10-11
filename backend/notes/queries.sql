select * from timesheet 
where dttimeenter between '8/aug/2021' and '13/aug/2021'
order by dttimeenter;

select * from approval order by timesheetid desc

insert into approval (timesheetid, userid, approval)
select 44 as timesheetid, 23 as userid, true as approval
union 
select 49, 23, true
union
select 48, 23, true
union
select 45, 23, true
union
select 47, 23, true
union
select 50, 23, true


select * from get_approved_timesheet('8/aug/2021', '13/aug/2021', 24)


insert into timesheet (userid, dttimeenter, inout)
select 24 as userid, '2021-08-09 08:00:00'::timestamp as dttimeenter, true as inout
union
select 24, '2021-08-09 18:00:00', false
union
select 24, '2021-08-09 17:50:00', false
union
select 24, '2021-08-10 07:00:00', true
union
select 24, '2021-08-10 09:00:00', true
union
select 24, '2021-08-10 19:00:00', false
union
select 24, '2021-08-12 09:00:00', true
union
select 24, '2021-08-12 17:30:00', false

select * from rf_user

delete from rf_user where userid in (32, 33)


insert into rf_user(username, firstname, lastname) select 'kzheng', 'karen', 'zheng'