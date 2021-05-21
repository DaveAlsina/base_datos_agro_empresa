def getMeasurements():

    """
    Input:  date_range = ['fecha inicial', 'fecha final']
            crop_name = 'nombre del cultivo'
    
    la fecha debe estar en formato yy-mm-dd 

    Output: si ambos argumentos son distintos del default 
            da un filtrado por fecha
    """

    # if (crop_name == "") and (date_range == []):
    return """select * from measurement;"""

    # if (crop_name != "") and (date_range == []):

    #     sql =  """select * from measurement 
    #               where sensor_id_sensor_info in (  select sensor_id from sensor_info
    #                                                 where id_zone in( select cr.id_zone from crop as cr
    #                                                                   where cr.name in ('{}')
    #                                                                 )
    #                                              );""".format(crop_name)
    #     return sql

    # if (crop_name != "") and (date_range != []):


    #     sql = """select * from measurement as m
    #              where sensor_id_sensor_info in ( select sensor_id from sensor_info
    #                                               where id_zone in( select cr.id_zone from crop as cr
    #                                                                  where cr.name in ('{}')
    #                                                                )
    #              ) and m.time between to_timestamp('{}', 'YYYY-MM-DD HH:MI:SS')
    #                and to_timestamp('{}', 'YYYY-MM-DD HH:MI:SS');""".format(crop_name, date_range[0], date_range[1]);

    #     return sql

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
    return """select opc.crop_name, cast(sum(sls.total_income) as float) as total_income
            from sales sls join crop cr on(sls.id_crop = cr.id) join optimum_condition opc on(cr.id_crop_name_optimum_condition = opc.id_crop_name)
            group by opc.crop_name"""
