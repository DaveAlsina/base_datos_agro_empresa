-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.2
-- PostgreSQL version: 12.0
-- Project Site: pgmodeler.io
-- Model Author: ---


-- Database creation must be done outside a multicommand file.
-- These commands were put in this file only as a convenience.
-- -- object: new_database | type: DATABASE --
-- -- DROP DATABASE IF EXISTS new_database;
-- CREATE DATABASE new_database;
-- -- ddl-end --
-- 

-- object: public.measurement | type: TABLE --
-- DROP TABLE IF EXISTS public.measurement CASCADE;
CREATE TABLE public.measurement (
	sensor_id_sensor_info integer NOT NULL,
	"time" timestamp NOT NULL,
	temperature numeric(4,2),
	humidity numeric(4,2),
	pressure numeric(6,2),
	lux numeric(7,2),
	electroconductivity numeric(4,3),
	CONSTRAINT measurement_pk PRIMARY KEY ("time",sensor_id_sensor_info)

);
-- ddl-end --
-- ALTER TABLE public.measurement OWNER TO postgres;
-- ddl-end --

-- object: public.zone | type: TABLE --
-- DROP TABLE IF EXISTS public.zone CASCADE;
CREATE TABLE public.zone (
	id serial NOT NULL,
	name varchar(45) NOT NULL,
	CONSTRAINT zone_pk PRIMARY KEY (id),
	CONSTRAINT name_unique UNIQUE (name)

);
-- ddl-end --
-- ALTER TABLE public.zone OWNER TO postgres;
-- ddl-end --

-- object: public.sensor_info | type: TABLE --
-- DROP TABLE IF EXISTS public.sensor_info CASCADE;
CREATE TABLE public.sensor_info (
	sensor_id integer NOT NULL,
	name varchar(15) NOT NULL,
	id_zone integer NOT NULL,
	CONSTRAINT sensor_ubication_pk PRIMARY KEY (sensor_id)

);
-- ddl-end --
-- ALTER TABLE public.sensor_info OWNER TO postgres;
-- ddl-end --

-- object: public.sales | type: TABLE --
-- DROP TABLE IF EXISTS public.sales CASCADE;
CREATE TABLE public.sales (
	id serial NOT NULL,
	date date NOT NULL,
	quantity real NOT NULL,
	total_income real NOT NULL,
	id_crop integer NOT NULL,
	id_unit_measurement_eqv integer NOT NULL,
	CONSTRAINT sales_pk PRIMARY KEY (id)

);
-- ddl-end --
-- ALTER TABLE public.sales OWNER TO postgres;
-- ddl-end --

-- object: public.crop | type: TABLE --
-- DROP TABLE IF EXISTS public.crop CASCADE;
CREATE TABLE public.crop (
	id serial NOT NULL,
	id_crop_name_optimum_condition integer NOT NULL,
	start_date timestamp NOT NULL,
	end_date timestamp,
	id_zone integer,
	id_production integer,
	CONSTRAINT crop_pk PRIMARY KEY (id)

);
-- ddl-end --
-- ALTER TABLE public.crop OWNER TO postgres;
-- ddl-end --

-- object: public.production | type: TABLE --
-- DROP TABLE IF EXISTS public.production CASCADE;
CREATE TABLE public.production (
	id serial NOT NULL,
	planting_area real NOT NULL,
	harvest_area real,
	production_t real,
	performance_crop real,
	CONSTRAINT production_pk PRIMARY KEY (id)

);
-- ddl-end --
-- ALTER TABLE public.production OWNER TO postgres;
-- ddl-end --

-- object: zone_fk | type: CONSTRAINT --
-- ALTER TABLE public.crop DROP CONSTRAINT IF EXISTS zone_fk CASCADE;
ALTER TABLE public.crop ADD CONSTRAINT zone_fk FOREIGN KEY (id_zone)
REFERENCES public.zone (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: production_fk | type: CONSTRAINT --
-- ALTER TABLE public.crop DROP CONSTRAINT IF EXISTS production_fk CASCADE;
ALTER TABLE public.crop ADD CONSTRAINT production_fk FOREIGN KEY (id_production)
REFERENCES public.production (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.expenses | type: TABLE --
-- DROP TABLE IF EXISTS public.expenses CASCADE;
CREATE TABLE public.expenses (
	id serial NOT NULL,
	date date NOT NULL,
	amount real NOT NULL,
	info varchar(45),
	id_expense_category integer NOT NULL,
	id_crop integer NOT NULL,
	CONSTRAINT expenses_pk PRIMARY KEY (id)

);
-- ddl-end --
-- ALTER TABLE public.expenses OWNER TO postgres;
-- ddl-end --

-- object: zone_fk | type: CONSTRAINT --
-- ALTER TABLE public.sensor_info DROP CONSTRAINT IF EXISTS zone_fk CASCADE;
ALTER TABLE public.sensor_info ADD CONSTRAINT zone_fk FOREIGN KEY (id_zone)
REFERENCES public.zone (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.optimum_condition | type: TABLE --
-- DROP TABLE IF EXISTS public.optimum_condition CASCADE;
CREATE TABLE public.optimum_condition (
	id_crop_name serial NOT NULL,
	crop_name varchar(45) NOT NULL,
	min_humidity smallint,
	max_humidity smallint,
	min_temperature_day numeric(4,2),
	max_temperature_day numeric(4,2),
	min_temperature_night numeric(4,2),
	max_temperature_night numeric(4,2),
	min_ec numeric(4,2),
	max_ec numeric(4,2),
	CONSTRAINT uniq_crop_name UNIQUE (crop_name),
	CONSTRAINT optimum_condition_pk PRIMARY KEY (id_crop_name)

);
-- ddl-end --
-- ALTER TABLE public.optimum_condition OWNER TO postgres;
-- ddl-end --

-- object: crop_fk | type: CONSTRAINT --
-- ALTER TABLE public.expenses DROP CONSTRAINT IF EXISTS crop_fk CASCADE;
ALTER TABLE public.expenses ADD CONSTRAINT crop_fk FOREIGN KEY (id_crop)
REFERENCES public.crop (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: crop_fk | type: CONSTRAINT --
-- ALTER TABLE public.sales DROP CONSTRAINT IF EXISTS crop_fk CASCADE;
ALTER TABLE public.sales ADD CONSTRAINT crop_fk FOREIGN KEY (id_crop)
REFERENCES public.crop (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: optimum_condition_fk | type: CONSTRAINT --
-- ALTER TABLE public.crop DROP CONSTRAINT IF EXISTS optimum_condition_fk CASCADE;
ALTER TABLE public.crop ADD CONSTRAINT optimum_condition_fk FOREIGN KEY (id_crop_name_optimum_condition)
REFERENCES public.optimum_condition (id_crop_name) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.expense_category | type: TABLE --
-- DROP TABLE IF EXISTS public.expense_category CASCADE;
CREATE TABLE public.expense_category (
	id serial NOT NULL,
	name varchar(40) NOT NULL,
	CONSTRAINT expense_category_pk PRIMARY KEY (id),
	CONSTRAINT uniq_category_name UNIQUE (name)

);
-- ddl-end --
-- ALTER TABLE public.expense_category OWNER TO postgres;
-- ddl-end --

-- object: expense_category_fk | type: CONSTRAINT --
-- ALTER TABLE public.expenses DROP CONSTRAINT IF EXISTS expense_category_fk CASCADE;
ALTER TABLE public.expenses ADD CONSTRAINT expense_category_fk FOREIGN KEY (id_expense_category)
REFERENCES public.expense_category (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.unit_measurement_eqv | type: TABLE --
-- DROP TABLE IF EXISTS public.unit_measurement_eqv CASCADE;
CREATE TABLE public.unit_measurement_eqv (
	id serial NOT NULL,
	unit varchar(45) NOT NULL,
	eqv_kg integer NOT NULL,
	CONSTRAINT unit_measurement_eqv_pk PRIMARY KEY (id),
	CONSTRAINT uq_unit UNIQUE (unit)

);
-- ddl-end --
-- ALTER TABLE public.unit_measurement_eqv OWNER TO postgres;
-- ddl-end --

-- object: unit_measurement_eqv_fk | type: CONSTRAINT --
-- ALTER TABLE public.sales DROP CONSTRAINT IF EXISTS unit_measurement_eqv_fk CASCADE;
ALTER TABLE public.sales ADD CONSTRAINT unit_measurement_eqv_fk FOREIGN KEY (id_unit_measurement_eqv)
REFERENCES public.unit_measurement_eqv (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: sensor_info_fk | type: CONSTRAINT --
-- ALTER TABLE public.measurement DROP CONSTRAINT IF EXISTS sensor_info_fk CASCADE;
ALTER TABLE public.measurement ADD CONSTRAINT sensor_info_fk FOREIGN KEY (sensor_id_sensor_info)
REFERENCES public.sensor_info (sensor_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --


