-- Table: public.rf_config

-- DROP TABLE IF EXISTS public.rf_config;

CREATE TABLE public.rf_config
(
    configid integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    parameter character varying(100) COLLATE pg_catalog."default" NOT NULL,
    parameter_value character varying COLLATE pg_catalog."default" NOT NULL,
    dtstart date NOT NULL DEFAULT now(),
    CONSTRAINT rf_config_pkey PRIMARY KEY (configid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.rf_config
    OWNER to postgres;
-- Index: idx_config_parameter

-- DROP INDEX IF EXISTS public.idx_config_parameter;

CREATE INDEX idx_config_parameter
    ON public.rf_config USING btree
    (parameter COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;



-- Table: public.rf_role

-- DROP TABLE IF EXISTS public.rf_role;

CREATE TABLE public.rf_role
(
    roleid integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    role character varying(60) COLLATE pg_catalog."default" NOT NULL,
    description character varying(200) COLLATE pg_catalog."default",
    CONSTRAINT rf_role_pkey PRIMARY KEY (roleid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.rf_role
    OWNER to postgres;


-- Table: public.rf_special_day

-- DROP TABLE IF EXISTS public.rf_special_day;

CREATE TABLE public.rf_special_day
(
    dayid integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    dte date NOT NULL,
    description character varying(100) COLLATE pg_catalog."default",
    holiday boolean NOT NULL DEFAULT true,
    CONSTRAINT rf_special_days_pkey PRIMARY KEY (dayid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.rf_special_day
    OWNER to postgres;


-- Table: public.rf_user

-- DROP TABLE IF EXISTS public.rf_user;

CREATE TABLE public.rf_user
(
    userid integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    username character varying(60) COLLATE pg_catalog."default" NOT NULL,
    firstname character varying(60) COLLATE pg_catalog."default" NOT NULL,
    lastname character varying(60) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT rf_user_pkey PRIMARY KEY (userid, username),
    CONSTRAINT rf_user_userid_key UNIQUE (userid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.rf_user
    OWNER to postgres;


-- Table: public.user_roles

-- DROP TABLE IF EXISTS public.user_roles;

CREATE TABLE public.user_roles
(
    userid integer NOT NULL,
    roleid integer NOT NULL,
    dtstart date NOT NULL DEFAULT now(),
    valid boolean DEFAULT true,
    CONSTRAINT user_roles_pkey PRIMARY KEY (userid, roleid, dtstart),
    CONSTRAINT user_roles_rf_role FOREIGN KEY (roleid)
        REFERENCES public.rf_role (roleid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT user_roles_rf_user FOREIGN KEY (userid)
        REFERENCES public.rf_user (userid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_roles
    OWNER to postgres;


-- Table: public.timesheet

-- DROP TABLE IF EXISTS public.timesheet;

CREATE TABLE public.timesheet
(
    timesheetid integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    userid integer NOT NULL,
    dttimeenter timestamp without time zone NOT NULL DEFAULT now(),
    "inout" boolean,
    CONSTRAINT timesheetid_pkey PRIMARY KEY (timesheetid),
    CONSTRAINT timesheet_rf_user FOREIGN KEY (userid)
        REFERENCES public.rf_user (userid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.timesheet
    OWNER to postgres;


-- Table: public.approval

-- DROP TABLE IF EXISTS public.approval;

CREATE TABLE public.approval
(
    timesheetid integer NOT NULL,
    userid integer NOT NULL,
    dttimeenter timestamp without time zone NOT NULL DEFAULT now(),
    approval boolean DEFAULT true,
    CONSTRAINT approval_pkey PRIMARY KEY (timesheetid),
    CONSTRAINT approval_timesheet FOREIGN KEY (timesheetid)
        REFERENCES public.timesheet (timesheetid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT user_roles_rf_user FOREIGN KEY (userid)
        REFERENCES public.rf_user (userid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.approval
    OWNER to postgres;



INSERT INTO rf_role (role, description) 
select 'admin' as role, 'Admin' as description
union 
select 'driver', 'Driver';

INSERT INTO rf_config (parameter, parameter_value)
select 'ot_hourly_rate' as parameter, 15000 as parameter_value
union
select 'daily_allowance', 100000
union
select 'ot_allowance', 200000;



INSERT INTO rf_user (username, firstname, lastname)
select 'admin' as username, 'Admin' as firstname, 'trator' as lastname
union
select 'endang', 'Endang', 'Wahyudin';


insert into user_roles (userid, roleid)
select 1 as userid, 1 as roleid
union
select 2, 2;