# DNS-Script-con-IA

Desarrollo de una Aplicación en Python para Auditoría DNS (Básico y  Avanzado) con Shodan

# Descripción General

Construir la aplicación (script o pequeña herramienta) en Python que realice un análisis de servidores DNS en dos niveles:

1. Básico – Búsqueda simple y verificación de IPs con servidor DNS expuesto. 
2. Avanzado – Implementación de funcionalidades extras (verificación de  recursividad, amplificación DNS, paginación o múltiples dominios, etc.) e integración de Shodan u otra herramienta similar que aporte datos de red.
3. Nota: cualquier otra función avanzada que considere y/o investigue el estudiante. Check de sistemas o DNS seguros publicados etc.

Asimismo, se solicita que cada estudiante construya y documento el “prompt” o conjunto de instrucciones que utilizaron con la(s) herramienta(s) de IA o de red (p. ej. ChatGPT, Bard, Bing Chat, etc.) para generar o refinar el código, y el alcance que se espera de la aplicación.

# Alcance y Requerimientos

* Lenguaje: Python 3.x 
* Bibliotecas: shodan, dnspython, requests (o equivalentes)
* Herramienta: Shodan (u otra API/herramienta de recolección de datos de red) para obtener IPs expuestas en puerto 53. 
* Prompt: El estudiante deberá documentar y mostrar exactamente cómo formuló las preguntas o instrucciones en la(s) herramienta(s) de IA utilizadas (como ChatGPT, Bing, Bard, etc.).
* Funciones Básicas:
```
o Búsqueda de IPs con DNS expuesto (básico).
o Verificación de resolución DNS (por ejemplo, a un dominio específico).
```
* Funciones Avanzadas (al menos dos de las siguientes):
```
o Verificación de recursividad.
o Detección de amplificación DNS.
o Paginación en Shodan (o herramienta alternativa).
o Múltiples dominios de prueba.
o Integración de lista negra (blacklist).
```
# Manual de Uso: Script de Conexión y Consulta a InfluxDB "influxconnection.py"

- Manual para la prueba de conexión de python con InfluxDB

## 1. Descripción General

Este script en Python permite conectar con una instancia de InfluxDB 2.x, escribir datos en un bucket y posteriormente realizar una consulta para obtener esos datos.

## 2. Requisitos Previos

Antes de ejecutar el script, asegúrese de cumplir con los siguientes requisitos:

* Tener InfluxDB 2.x instalado y en ejecución.
* Contar con un bucket configurado en InfluxDB.
* Tener una API Token de InfluxDB con permisos de escritura y lectura.
* Python 3.7 o superior instalado.
* Instalar las dependencias necesarias.

## 3. Instalación

- Ejecute el siguiente comando en el CMD para instalar la librería requerida:
```
pip install influxdb-client
```
- Instale InfluxDB 2.x en su máquina host, si es windows descargue en la terminal de powershell:
```
- InfluxDB OSS 2.x
- wget https://download.influxdata.com/influxdb/releases/influxdb2-2.7.11-windows.zip -UseBasicParsing -OutFile influxdb2-2.7.11-windows.zip
- Expand-Archive .\influxdb2-2.7.11-windows.zip -DestinationPath 'C:\Program Files\InfluxData\influxdb\'
```
- Vaya a la direccion: 'C:\Program Files\InfluxData\influxdb\' y ejecute: .\influxd.exe
```
Luego de estar funcionando el influx diríjase al navegador y escriba: "http://localhost:8086"
Una vez dentro cree su TOKEN, ORGANIZACION y BUCKET
```

## 4. Configuración

Antes de ejecutar el script, edite las siguientes variables para adaptarlas a su entorno:
```
INFLUXDB_URL = "http://localhost:8086"  # URL del servidor InfluxDB
INFLUXDB_TOKEN = "XXXXXXXXXXXXXXXXXXXXXX"  # Reemplace con su token de autenticación
INFLUXDB_ORG = ""  # Nombre de la organización
INFLUXDB_BUCKET = ""  # Nombre del bucket donde se almacenarán los datos
```

## 5. Ejecución del Script

Para ejecutar el script, simplemente ejecute el siguiente comando en la terminal:
```
python script.py
```

El script realizará las siguientes acciones:

* Conectar con InfluxDB usando las credenciales configuradas.
* Escribir cinco puntos de datos en la serie temporal con la medición measurement1.
* Realizar una consulta para obtener los datos escritos en los últimos 10 minutos.
* Imprimir los resultados en la consola.

## 6. Interpretación de los Resultados

Al ejecutar el script, debería ver una salida similar a la siguiente en la terminal:
```
📡 Escribiendo punto 0 en InfluxDB
📡 Escribiendo punto 1 en InfluxDB
📡 Escribiendo punto 2 en InfluxDB
📡 Escribiendo punto 3 en InfluxDB
📡 Escribiendo punto 4 en InfluxDB
✅ Datos escritos en InfluxDB con éxito.
📡 Tiempo: 2025-03-26T12:34:56.789Z, Valor: 0
📡 Tiempo: 2025-03-26T12:34:57.789Z, Valor: 1
📡 Tiempo: 2025-03-26T12:34:58.789Z, Valor: 2
📡 Tiempo: 2025-03-26T12:34:59.789Z, Valor: 3
📡 Tiempo: 2025-03-26T12:35:00.789Z, Valor: 4

```
- Una vez ejecutada se dará por confirmada la conexión a influx y se podrá seguir con la configuracion de Grafana
  El objetivo es registrar interactivamente en un Dashboard las Ip de los DNS en tiempo real y tener una mejora en la visualización y/o registro.
- Antes de integrar Grafana, se explicará el codigo de prueba de registro de Ip's en influx: **"influxIPs.py"**

# Manual de Uso: Script **"influxIPs.py"**

## Inicialización del Cliente de InfluxDB

