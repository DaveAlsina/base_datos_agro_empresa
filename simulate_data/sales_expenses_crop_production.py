import csv
import random
# import datetime
import numpy as np
import pandas as pd

fieldnames1=['id','date','unit_measurement','quantity', 'price_per_unit', 'total_income']
writer = csv.DictWriter(open("sales.csv", "w", newline = ''), fieldnames=fieldnames1)

base_date = np.datetime64('2020-06-24')


n1 = 9890

writer.writerow(dict(zip(fieldnames1, fieldnames1)))
for i in range(n1):
    unit = random.choice([200, 300])
    if unit == 200:
        price = 1200
    else:
        price = 1400
    q = random.randint(20, 60)
    writer.writerow(dict([
      ('id', i+110),
      ('date', base_date + np.random.choice(300)),
      ('unit_measurement', unit),
      ('quantity', q),
      ('price_per_unit', price),
      ('total_income', price*q)]))


df_sales = pd.read_csv("sales.csv")
df_sales = df_sales.sort_values(by="date")
df_sales.to_csv(r'.\sales_final.csv', index = False, header=True)


fieldnames2 = ['id', 'date', 'amount', 'info']
writer = csv.DictWriter(open("expenses.csv", "w", newline = ''), fieldnames=fieldnames2)


n2 = 7850

writer.writerow(dict(zip(fieldnames2, fieldnames2)))
for i in range(n2):
    writer.writerow(dict([
      ('id', i+1010),
      ('date', base_date + np.random.choice(300)),
      ('amount', round(random.randint(10000, 200000)/100)*100)]))
    

df_exp = pd.read_csv("expenses.csv")
df_exp = df_exp.sort_values(by="date")
df_exp.to_csv(r'.\expenses_final.csv', index = False, header=True)


fieldnames3 = ['id', 'plating_area', 'harvest_area', 'production_t', 'performance_crop']
writer = csv.DictWriter(open("production.csv", "w", newline = ''), fieldnames=fieldnames3)

n3 = 30

writer.writerow(dict(zip(fieldnames3, fieldnames3)))
for i in range(n3):
    ha = random.randint(2, 4)
    t = random.randint(1, 3)
    writer.writerow(dict([
      ('id', i+10),
      ('plating_area', random.randint(2, 5)),
      ('harvest_area', ha),
      ('production_t', t),
      ('performance_crop', t/ha)]))

   
# Fuente: https://www.datos.gov.co/Agricultura-y-Desarrollo-Rural/Producci-n-Agr-cola-consolidada-en-el-2016/9wzr-qgme
# cantidad de datos
n4 = 30
# lista de dias
fecha_final = np.datetime64('2021-05-10')
fecha_inicial = np.datetime64('2020-06-24') 
delta_dias = (fecha_final - fecha_inicial).astype(int)
diff_dias = np.linspace(0,delta_dias,n4).astype(int)


fieldnames4 = ['id', 'start_date', 'end_date']
writer = csv.DictWriter(open("crop.csv", "w", newline = ''), fieldnames=fieldnames4)
writer.writerow(dict(zip(fieldnames4, fieldnames4)))


def set_format(ts):
    res = str(ts)
    res= res.replace("-", "/")
    res = res.replace("T", " ")
    anio = res[0:4]
    mes = res[5:7]
    dia = res[8:10]
    final = mes+"/"+dia+"/"+anio+ res[10:]
    return final

for i in range(n4):
    h_start, h_end = random.choices(np.arange(0,23,1),k=2)
    m_start, m_end = random.choices(np.arange(0,59,1),k=2)

    
    # Correcion de formato de hora a 'HH:MM'
    h_start = str(h_start)
    h_end= str(h_end)
    m_start = str(m_start)
    m_end= str(m_end)
    
    if len(h_start) == 1:
        h_start = '0' + h_start
    
    if len(h_end) == 1:
        h_end= '0' + h_end

    if len(m_start) == 1:
        m_start = '0'+ m_start

    if len(m_end) == 1:
        m_end= '0'+ m_end
    
    f_ini_i = np.datetime64(str(fecha_inicial+diff_dias[i]) +'T'+h_start+':'+m_start)
    # Se crea la fecha final sumando un numero aleatorio de dias enttre 15 y 30 dias
    duracion = random.choice(range(15,30))
    f_end_i = f_ini_i + np.timedelta64(duracion, 'D')
    f_end_i = np.datetime64(str(f_end_i)[:11] + h_end + ":" + m_end)
    
    # Correcciones a formato final
    f_ini_i = set_format(f_ini_i)
    f_end_i = set_format(f_end_i)
    
    writer.writerow(dict([
        ('id', i+100001),
        ('start_date', f_ini_i),
        ('end_date', f_end_i) ]))




















