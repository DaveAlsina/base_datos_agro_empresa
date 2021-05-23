def createMeasurement_selection_menu():

    """
    Función encargada de devolver cuales son los cultivos que 
    tienen datos asociados para mostrarse en el display de measuments
    esta función se encarga de invocar una función que fue definida
    internamente en sql por conveniencia
    """

    return """select * from get_crops_with_measurements(get_min_date_measurement(), get_max_date_measurement())"""

def getMeasurements(crop_name = "", start_date = "", date_range =[]):

    """
    Input:  start_date = "fecha de inicio del cultivo"
            date_range = ['fecha inicial', 'fecha final']
            crop_name = 'nombre del cultivo'
    
    la fecha debe estar en formato yy-mm-dd 

    Output: si ambos argumentos son distintos del default 
            da un filtrado por fecha
    """

    if ((crop_name != "") and (start_date != "")):
        return """select * from get_crop_measurements('{}', '{}');""".format(crop_name, start_date)

    else:

        return """select * from measurement;"""


def getCrop():
    return """select * from crop;"""

def getExpCategory():
    return """select * from expense_category;"""

def getExpenses():
    return """select * from expenses;"""

def getOptCondition():
    return """select * from optimum_condition;"""

def getSales():
    return """select * from sales;"""

def getSensInfo():
    return """select * from sensor_info;"""

def getUnit():
    return """select * from unit_measurement_eqv;"""

def getZone():
    return """select * from zone;"""
  
def getProduction():
    return """select * from production;"""

def getTotalIncomeByCrop():
    return """select opc.crop_name as crop, cast(sum(sls.total_income) as float) as total_income
from sales sls join crop cr on(sls.id_crop = cr.id) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
group by crop"""

def getTotalProdSoldByCrop():
    return """select opc.crop_name as crop, cast(sum(sls.quantity)/1000000 as float) as total_tons
from sales sls join crop cr on(sls.id_crop = cr.id) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
group by crop"""

#EL NOMBRE DEL CULTIVO SE DEBE INGRESAR EN COMILLAS "lechuga" O "cilantro" COMO PARÁMETRO
def getPercHum(nombre_cultivo):
    return """select optimum_condition.crop_name, ((select (select count(crop.id) as count_m
	from ((((optimum_condition as opt_c inner join crop on opt_c.id_crop_name = crop.id_crop_name_optimum_condition)
    inner join zone on crop.id_zone = zone.id)
    inner join sensor_info on zone.id = sensor_info.id_zone)
    inner join measurement on sensor_info.sensor_id = measurement.sensor_id_sensor_info)
    WHERE opt_c.crop_name = '{0}'
	AND measurement.humidity BETWEEN (
								SELECT min_humidity
								FROM optimum_condition
								WHERE crop_name = '{0}')
								AND
								(
								SELECT max_humidity
								FROM optimum_condition
								WHERE crop_name = '{0}'))*100) / (select count(crop.id) as total_crop
	from ((((optimum_condition as opt_c inner join crop on opt_c.id_crop_name = crop.id_crop_name_optimum_condition)
    inner join zone on crop.id_zone = zone.id)
    inner join sensor_info on zone.id = sensor_info.id_zone)
    inner join measurement on sensor_info.sensor_id = measurement.sensor_id_sensor_info)
    WHERE opt_c.crop_name = '{0}')) as percentage
	FROM optimum_condition
	WHERE crop_name = '{0}'""".format(nombre_cultivo)

def getPercEc(nombre_cultivo):
    return """select optimum_condition.crop_name, ((select (select count(crop.id) as count_m
	from ((((optimum_condition as opt_c inner join crop on opt_c.id_crop_name = crop.id_crop_name_optimum_condition)
    inner join zone on crop.id_zone = zone.id)
    inner join sensor_info on zone.id = sensor_info.id_zone)
    inner join measurement on sensor_info.sensor_id = measurement.sensor_id_sensor_info)
    WHERE opt_c.crop_name = '{0}'
	AND measurement.electroconductivity BETWEEN (
								SELECT min_ec
								FROM optimum_condition
								WHERE crop_name = '{0}')
								AND
								(
								SELECT max_ec
								FROM optimum_condition
								WHERE crop_name = '{0}'))*100) / (select count(crop.id) as total_crop
	from ((((optimum_condition as opt_c inner join crop on opt_c.id_crop_name = crop.id_crop_name_optimum_condition)
    inner join zone on crop.id_zone = zone.id)
    inner join sensor_info on zone.id = sensor_info.id_zone)
    inner join measurement on sensor_info.sensor_id = measurement.sensor_id_sensor_info)
    WHERE opt_c.crop_name = '{0}')) as percentage
	FROM optimum_condition
	WHERE crop_name = '{0}'""".format(nombre_cultivo)

def getPercTempD(nombre_cultivo, fecha):
    return """select optimum_condition.crop_name, ((select (select count(crop.id) as count_m
	from ((((optimum_condition as opt_c inner join crop on opt_c.id_crop_name = crop.id_crop_name_optimum_condition)
    inner join zone on crop.id_zone = zone.id)
    inner join sensor_info on zone.id = sensor_info.id_zone)
    inner join measurement on sensor_info.sensor_id = measurement.sensor_id_sensor_info)
    WHERE opt_c.crop_name = '{0}'
    AND time IN (SELECT time
	 FROM measurement
	 WHERE (SELECT EXTRACT(hour from time)) >= 06 
	 AND (SELECT EXTRACT(hour from time)) < 18 
	 AND time::date >= '{1}')
	AND measurement.humidity BETWEEN (
								SELECT min_humidity
								FROM optimum_condition
								WHERE crop_name = '{0}')
								AND
								(
								SELECT max_humidity
								FROM optimum_condition
								WHERE crop_name = '{0}'))*100) / (select count(crop.id) as total_crop
	from ((((optimum_condition as opt_c inner join crop on opt_c.id_crop_name = crop.id_crop_name_optimum_condition)
    inner join zone on crop.id_zone = zone.id)
    inner join sensor_info on zone.id = sensor_info.id_zone)
    inner join measurement on sensor_info.sensor_id = measurement.sensor_id_sensor_info)
    WHERE opt_c.crop_name = '{0}')) as percentage
	FROM optimum_condition
	WHERE crop_name = '{0}'""".format(nombre_cultivo, fecha)

def getPercTempN(nombre_cultivo, fecha):
    return """select optimum_condition.crop_name, ((select (select count(crop.id) as count_m
	from ((((optimum_condition as opt_c inner join crop on opt_c.id_crop_name = crop.id_crop_name_optimum_condition)
    inner join zone on crop.id_zone = zone.id)
    inner join sensor_info on zone.id = sensor_info.id_zone)
    inner join measurement on sensor_info.sensor_id = measurement.sensor_id_sensor_info)
    WHERE opt_c.crop_name = '{0}'
    AND time IN (SELECT time
	 FROM measurement
	 WHERE ((SELECT EXTRACT(hour from time)) > 18 
	 AND (SELECT EXTRACT(hour from time)) <= 23)
		OR
		((SELECT EXTRACT(hour from time)) >= 00
		AND (SELECT EXTRACT(hour from time)) < 06) 
	 AND time::date >= '{1}')
	AND measurement.humidity BETWEEN (
								SELECT min_humidity
								FROM optimum_condition
								WHERE crop_name = '{0}')
								AND
								(
								SELECT max_humidity
								FROM optimum_condition
								WHERE crop_name = '{0}'))*100) / (select count(crop.id) as total_crop
	from ((((optimum_condition as opt_c inner join crop on opt_c.id_crop_name = crop.id_crop_name_optimum_condition)
    inner join zone on crop.id_zone = zone.id)
    inner join sensor_info on zone.id = sensor_info.id_zone)
    inner join measurement on sensor_info.sensor_id = measurement.sensor_id_sensor_info)
    WHERE opt_c.crop_name = '{0}')) as percentage
	FROM optimum_condition
	WHERE crop_name = '{0}'""".format(nombre_cultivo, fecha)



