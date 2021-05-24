## sales

def getTotalIncomeByCrop():
    return """select opc.crop_name as cultivo, sum(sls.total_income)::float as ingresos_totales
        from sales sls join crop cr on(sls.id_crop = cr.id) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
        group by cultivo"""

def getTotalProdSoldByCrop():
    return """select opc.crop_name as cultivo, cast(sum(sls.quantity)/1000000 as float) as toneladas_totales
        from sales sls join crop cr on(sls.id_crop = cr.id) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
        group by cultivo"""


def getTimeSeriesSales():
    return """select date as fecha, sum(total_income)::float as ingresos_totales
from sales
group by fecha
order by fecha asc"""

def getTimeSeriesTons():
    return """select date as fecha, sum(quantity)::float/1000000 as toneladas
        from sales
        group by fecha
        order by fecha asc"""


def getSalesbyZone():
    return """select z.name as zona, sum(sls.total_income)::float as ingresos_totales
        from sales sls join crop cr on(sls.id_crop = cr.id) join zone z on(cr.id_zone = z.id)
        group by zona"""
        
        
def StatIncome():
    return """select 'total' as est_des,
    sum(total_income)::float as ventas
    from sales
    union all
    select 'promedio',
    round(avg(total_income)::numeric,1)
    from sales
    union all
    select 'min',
    min(total_income)
    from sales
    union all
    select 'max',
    max(total_income)
    from sales"""
    
    
## expenses
    

def getTotalExpensesByCrop():
    return """select opc.crop_name as cultivo, sum(ex.amount)::float as monto_gasto
    from expenses ex join crop cr on(ex.id_crop = cr.id) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
    group by cultivo"""


def getTimeSeriesExpenses():
    return """select date as fecha, sum(amount)::float as monto_gasto
    from expenses
    group by fecha
    order by fecha asc"""
    
def getExpensesCategory():
    return """select exc.name as categoria, sum(ex.amount)::float as monto_gasto
    from expenses ex join expense_category exc on(ex.id_expense_category = exc.id)
    group by categoria"""
    
def StatExpenses():
    return """select 'total' as est_des,
    sum(amount)::float as gastos
    from expenses
    union all
    select 'promedio',
    round(avg(amount)::numeric,1)
    from expenses
    union all
    select 'min',
    min(amount)
    from expenses
    union all
    select 'max',
    max(amount)
    from expenses"""

def getExpensesbyZone():
    return """select z.name as zona, sum(ex.amount)::float as monto_gasto
        from expenses ex join crop cr on(ex.id_crop = cr.id) join zone z on(cr.id_zone = z.id)
        group by zona"""

### ventas vs gastos
        
def getTotalSalesExpenses():
    return """select 'ingresos totales' as tipo,
    sum(total_income)::float as total
	from sales
	union all
	select 'gastos totales',
    sum(amount)::float
	from expenses"""
    
    
### produccion

def getProdByCrop():
    return """select opc.crop_name as cultivo, round(sum(pd.production_t)::numeric,2) as produccion_toneladas
    from production pd join crop cr on(pd.id = cr.id_production) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
    group by cultivo"""

def getHaByCrop():
    return """select opc.crop_name as cultivo, round(sum(pd.harvest_area)::numeric,2) as hectareas_cosechadas
    from production pd join crop cr on(pd.id = cr.id_production) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
    group by cultivo"""
    
def RendLechuga():
    return """select cr.end_date::date as fecha,  pd.performance_crop as rendimiento_lechuga
    from production pd join crop cr on(pd.id = cr.id_production) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
    where opc.crop_name = 'lechuga'"""

def RendCilantro():
    return """select cr.end_date::date as fecha, pd.performance_crop as rendimiento_cilantro
    from production pd join crop cr on(pd.id = cr.id_production) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
    where opc.crop_name = 'cilantro'"""

def ProdByZone():
    return """select z.name as zona, round(sum(pd.production_t)::numeric,2) as produccion_toneladas
    from production pd join crop cr on(pd.id = cr.id_production) join zone z on(cr.id_zone = z.id)
    group by zona"""

### prod vs ven
    
def ProdVsSales():
    return """select cultivo, produccion_toneladas, toneladas_vendidas, round((toneladas_vendidas - produccion_toneladas)::numeric,2) as perdidas
    from (
            select opc.crop_name as cultivo, round(sum(pd.production_t)::numeric,2) as produccion_toneladas
            from production pd join crop cr on(pd.id = cr.id_production) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
            group by cultivo) as pd
    join
            (select opc.crop_name as cultivo1, round((sum(sls.quantity)/1000000)::numeric,2) as toneladas_vendidas
            from sales sls join crop cr on(sls.id_crop = cr.id) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
            group by cultivo1) as sls on (pd.cultivo = sls.cultivo1)"""
            
            
            
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
	
