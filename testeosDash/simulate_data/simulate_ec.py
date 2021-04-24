import math
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt

#para generar numeros aleatorios basados en una distribución 
#normal
from random import normalvariate, seed
import pandas as pd

seed(323131253495) 
data = pd.read_csv("./sensor_data.csv")

#get start time
start_time = data["timestamp"][0]


#agrega el .0 para poder hacer uso de metodos de una librería 
#para calcular la diferencia en tiempo
#start_time = start_time[:-1] + '.00'

start_time += '.00'
print(start_time)

secs_per_day = 24 * 60 * 60
ec = []


for i in range(len(data)):
    
    #seteo de la media y la desviación estándar deseada para
    #generar el número aleatorio
    noise = normalvariate(0.4, 0.06)
    time = data["timestamp"][i] + '.00'

    if i%1000 == 0:         #cada 1000 iteraciones cambia la semilla del generador
        seed(noise)
    
    #calculo de la diferencia de tiempo en segundos
    datetimeFormat = "%Y-%m-%d %H:%M:%S.%f"
    diff = datetime.datetime.strptime(time, datetimeFormat)\
            - datetime.datetime.strptime(start_time, datetimeFormat) 

    secs = diff.seconds
    secs += diff.days * 24 * 60 * 60

    #uso de la diferencia de tiempo en segundos para simular el ec en ese momento
    #las otras componentes se usan para generar ruido en la señal simulada de electroconductividad
    othr_component1 = math.cos( (secs * 2 * math.pi)/(secs_per_day*3) ) + noise 
    othr_component2 = abs(math.cos( secs * 2 * math.pi ) + noise )
    main_component = math.sin( (secs * 2 * math.pi)/(secs_per_day*3) ) + noise

    #centra la componente principal de la electroconductividad alrededor de 2
    main_component += 2

    #reduce la amplitud de la onda de electroconductividad para que no se aleje mucho de 
    #el punto deseado 2
    main_component += (0.03* main_component) + (0.01* othr_component1) + (0.01*othr_component2)


    ec.append(main_component)


plt.scatter(list(range(0, len(ec))), ec)
plt.show()

data["ec"] = ec
data.to_csv("sensor_data_ec_added.csv", index=False)



#indexing and selecting data from pandas dataframe:
#1) https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html






