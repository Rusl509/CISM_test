-- Table: public.opensky

-- DROP TABLE IF EXISTS public.opensky;

CREATE TABLE IF NOT EXISTS public.opensky
(
    callsign character varying COLLATE pg_catalog."default",
    "number" character varying COLLATE pg_catalog."default",
    icao24 character varying COLLATE pg_catalog."default",
    registration character varying COLLATE pg_catalog."default",
    typecode character varying COLLATE pg_catalog."default",
    origin character varying COLLATE pg_catalog."default",
    destination character varying COLLATE pg_catalog."default",
    firstseen timestamp without time zone,
    lastseen timestamp without time zone,
    day date,
    latitude_1 double precision,
    longitude_1 double precision,
    altitude_1 double precision,
    latitude_2 double precision,
    longitude_2 double precision,
    altitude_2 double precision
) PARTITION BY RANGE (day);

ALTER TABLE IF EXISTS public.opensky
    OWNER to postgres;

-- Partitions SQL

CREATE TABLE public.opensky_part_0 PARTITION OF public.opensky
    FOR VALUES FROM ('2016-01-01') TO ('2017-01-01');

ALTER TABLE IF EXISTS public.opensky_part_0
    OWNER to postgres;
CREATE TABLE public.opensky_part_1 PARTITION OF public.opensky
    FOR VALUES FROM ('2017-01-01') TO ('2018-01-01');

ALTER TABLE IF EXISTS public.opensky_part_1
    OWNER to postgres;
CREATE TABLE public.opensky_part_2 PARTITION OF public.opensky
    FOR VALUES FROM ('2018-01-01') TO ('2019-01-01');

ALTER TABLE IF EXISTS public.opensky_part_2
    OWNER to postgres;
CREATE TABLE public.opensky_part_3 PARTITION OF public.opensky
    FOR VALUES FROM ('2019-01-01') TO ('2020-01-01');

ALTER TABLE IF EXISTS public.opensky_part_3
    OWNER to postgres;
CREATE TABLE public.opensky_part_4 PARTITION OF public.opensky
    FOR VALUES FROM ('2020-01-01') TO ('2021-01-01');

ALTER TABLE IF EXISTS public.opensky_part_4
    OWNER to postgres;
CREATE TABLE public.opensky_part_5 PARTITION OF public.opensky
    FOR VALUES FROM ('2021-01-01') TO ('2022-01-01');

ALTER TABLE IF EXISTS public.opensky_part_5
    OWNER to postgres;
CREATE TABLE public.opensky_part_6 PARTITION OF public.opensky
    FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');

ALTER TABLE IF EXISTS public.opensky_part_6
    OWNER to postgres;
