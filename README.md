# Proyecto de Bases de Datos: Agro-empresa

Este proyecto desarrolla una base de datos para una agro empresa que permite almacenar 
información sobre las condiciones a las que se encuentra expuesto el cultivo, y contabilidad básica 
de la empresa, dicha base de datos en conjunción con python permite desarrollar análisis significativos 
sobre el estado de la empresa y los cultivos.

----

## **El proyecto se compone de las siguientes carpetas:**

### data: 
- Se encuentran los datos de cada tabla del modelo relacional.

### dashborad: 
- main.py para correr el programa
#### connection: 
- Tiene los scripts para hacer la conexión a la base de datos con postgres a través de python.

### documentation:
- Contiene documentación académica en donde se basa la simulación de los datos.

### simulate\_data:
- Registra los algortimos que utilizó para la simulación.

### upload\_data:
- Posee los archivos create\_table\_project.sql y load\_measurements\_project.sql que permite crear las tablas y cargar los datos en SQL.

## **Pasos para correr el proyecto:**

1. Entrar a la carpeta data descargar los archivos .csv. Luego, entrar a la carpeta upload data
para crear las tablas con el archivo create table project.sql y para cargar los datos a través
del archivo load measurements project.sql al pgAdmin.
2. Luego, entrar a la carpeta dashboard.
3. Modificar el archivo conn data.json con las credenciales del personalizado pgAdmin.
4. Correr las funciones extras o auxiliares del archivo funciones extras.sql en pgAdmin.
5. Por último, correr el archivo main.py.
