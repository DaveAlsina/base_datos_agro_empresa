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

    return """select * from get_crop_measurements('{}', '{}');""".format(crop_name, start_date)


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
