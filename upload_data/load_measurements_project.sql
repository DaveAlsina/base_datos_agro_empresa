copy zone(id, name)
from '../data/zone.csv'
delimiter ','
csv header;

copy unit_measurement_eqv(id, unit, eqv_kg)
from '../data/unit_measurement_eqv.csv'
delimiter ','
csv header;

copy sensor_info(sensor_id, name, id_zone)
from '../data/sensor_info.csv'
delimiter ','
csv header;

SET datestyle = mdy

copy optimum_condition(id_crop_name, crop_name, min_humidity, max_humidity, min_temperature_day,
                      max_temperature_day, min_temperature_night, max_temperature_night, min_ec,
                      max_ec)
from '../data/optimum_condition.csv'
delimiter ','
csv header;

copy production(id, planting_area, harvest_area, production_t, performance_crop)
from '/home/alejandra/Desktop/production.csv'
delimiter ','
csv header;

copy crop(id, id_crop_name_optimum_condition, start_date, end_date, id_zone, id_production)
from '../data/crop.csv'
delimiter ',' encoding 'ISO-8859-1'
csv header;

copy sales(id, date, quantity, total_income, id_crop, id_unit_measurement_eqv)
from '../data/sales.csv'
delimiter ','
csv header;

copy expense_category(id, name)
from '../data/expense_category.csv'
delimiter ','
csv header;

copy expenses(id, date, amount, info, id_expense_category, id_crop)
from '../data/expenses.csv'
delimiter ','
csv header;

copy measurement(sensor_id_sensor_info, time, temperature, humidity, pressure, lux,
                electroconductivity)
from '../data/measurement.csv'
delimiter ',' encoding 'ISO-8859-1'
csv header;
