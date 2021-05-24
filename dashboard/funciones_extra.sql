create or replace function get_crops_with_measurements(minDate date, maxDate date)
	returns table(crop_name varchar(50), crop_id integer, date_ date) 
	as
	'
	
	select opt_c.crop_name, crop_id, sdate
	from optimum_condition as opt_c
	inner join 
		(select distinct crp_sensor_date.crop_id, crp_sensor_date.sdate, id_crp_name
		from measurement as mea 
		inner join 
			(select sinfo.sensor_id, zn_crop.crop_id, sdate, id_crp_name
			 from sensor_info as sinfo inner join (select zone.id as zone_id, crop.id as crop_id, crop.start_date sdate, id_crop_name_optimum_condition as id_crp_name
												  from zone inner join crop
												  on crop.id_zone = zone.id) as zn_crop
			 on zn_crop.zone_id = sinfo.id_zone) 
			 as crp_sensor_date
			 on mea.sensor_id_sensor_info = crp_sensor_date.sensor_id
		 where sdate::date between minDate and maxDate) as crop_with_meas
	on opt_c.id_crop_name = crop_with_meas.id_crp_name;
	'
	language sql;
	
create or replace function get_min_date_measurement()
	returns date
	as 
	'
	select min(mea.time)::date
	from measurement as mea
	'
	language sql;
	
create or replace function get_max_date_measurement()
	returns date
	as 
	'
	select max(mea.time)::date
	from measurement as mea
	'
	language sql;
	
select * from get_crops_with_measurements(get_min_date_measurement(), get_max_date_measurement());

create or replace function get_crop_measurements(crop_name_ varchar(45), date_ date)
	returns table(time_ timestamp, temperature numeric(4,2), humidity numeric(4,2), pressure numeric(6,2), lux numeric(7,2), electroconductivity numeric(4,3))
	as
	'
	
		select time, temperature, humidity, pressure, lux, electroconductivity as ec
		from measurement as mea
		where mea.time::date >= date_
		and mea.sensor_id_sensor_info in (
			select sens_inf.sensor_id as sens_id
			from sensor_info as sens_inf 
			inner join 
				(select crp.id_zone 
				from crop as crp
				inner join 
					(select id_crop_name as id_crp_nm 
					from optimum_condition as opt_cond
					where opt_cond.crop_name = crop_name_) as id_crp_name
				on crp.id_crop_name_optimum_condition =  id_crp_name.id_crp_nm 
				where crp.start_date::date = date_) as zone_crp
			on sens_inf.id_zone = zone_crp.id_zone
		)
		
	'
	language sql;
	
select * from get_crop_measurements('lechuga', '2021-04-28');

