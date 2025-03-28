# Manual de Usuario - Auditoría DNS con Shodan y Telegram

## 1. Introducción

Este software permite auditar servidores DNS expuestos en Shodan, verificando si permiten recursividad o amplificación, notificando sobre vulnerabilidades mediante Telegram sin antes pasar por la pagina "https://www.abuseipdb.com/" y almacenando datos en InfluxDB para luego observarlos en Grafana.

## 2. Requisitos Previos

* Tener una cuenta en Shodan con una API Key activa.
* Un bot de Telegram con su token de acceso.
* Un servidor con InfluxDB instalado.
* Python 3.x con las siguientes librerías instaladas:
```
pip install shodan dnspython requests influxdb-client
```
## 3. Configuración

- 3.1. Configurar las Credenciales

Antes de ejecutar el script, edite las siguientes variables con sus credenciales:

* SHODAN_API_KEY = "SU_API_KEY"
* TELEGRAM_BOT_TOKEN = "SU_TELEGRAM_TOKEN"
* CHAT_ID = "SU_CHAT_ID"
* INFLUXDB_URL = "http://localhost:8086"
* INFLUXDB_TOKEN = "SU_INFLUXDB_TOKEN"
* INFLUXDB_ORG = "SU_ORG"
* INFLUXDB_BUCKET = "SU_BUCKET"

## 4. Ejecución del Script

Para iniciar la auditoría, simplemente ejecute:
```
python script_dns_audit.py
```
El script realizará las siguientes acciones:
1. Buscará servidores DNS abiertos en Shodan.
2. Verificará si pueden resolver dominios.
3. Analizará si permiten recursividad.
4. Detectará posible amplificación.
5. Notificará por Telegram si un servidor es vulnerable.
6. Almacenará los resultados en InfluxDB.
7. Generará un reporte de IPs vulnerables en archivos locales.

## 5. Resultados y Reportes

* Archivos Generados:
```
- resultados_dns.txt: Contiene los resultados de la auditoría.
- reporte_vulnerables.txt: IPs detectadas con vulnerabilidades.
```
* Notificaciones:
```
- Telegram recibe alertas con detalles de las IPs vulnerables segun https://www.abuseipdb.com/.
```
Base de Datos:
```
- Los datos se almacenan en InfluxDB y pueden ser visualizados en herramientas como Grafana.
```
## 6. ¡¡¡SEGURIDAD Y RECOMENDACIONES!!!

## Uso Responsable: No utilice este script sin autorización.
## Límites de Shodan: Respete los límites de API y evite bloqueos.
## Protección de Datos: No comparta su API Key ni credenciales.
## REALICE ESTA PRÁCTICA CON FINES EDUCATIVOS Y DE ENTENDIMIENTO, LA RAZON DE ESTE SCRIPT ES PODER BLOQUEAR SI LAS IPS OBTENIDAS LLEGAN A GENERAR COMPLICACIONES.



# Explicación del Código

## 1. Búsqueda de Servidores DNS

## 1. Búsqueda de Servidores DNS

El script consulta Shodan para encontrar servidores DNS abiertos en el puerto 53:
```
def buscar_dns_expuestos():
    resultados = api.search("port:53")
    return [match['ip_str'] for match in resultados['matches']]
```
## 2. Verificación de Resolución

Comprueba si el DNS responde consultas:
```
def verificar_resolucion_dns(ip, dominio="google.com"):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [ip]
    respuesta = resolver.resolve(dominio, "A")
    return True, respuesta
```
## 3. Detección de Recursividad y Amplificación

Se verifica si el servidor permite consultas recursivas o genera respuestas anormalmente grandes:
```
def verificar_recursividad(ip):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [ip]
    resolver.resolve("example.com", "A")
    return True

def detectar_amplificacion(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(consulta, (ip, 53))
    respuesta, _ = sock.recvfrom(512)
    return len(respuesta) > 150
```
## 4. Notificaciones en Telegram

Si un servidor es vulnerable, se envía una alerta:
```
def enviar_alerta_telegram(ip, detalles):
    mensaje = f"🚨 DNS Inseguro Detectado: {ip}\n{detalles}"
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": mensaje})
```
## 5. Registro en InfluxDB

Los resultados se almacenan para análisis posterior:
```
def registrar_ip_en_influx(ip, recursividad, amplificacion):
    point = Point("dns_vulnerable").tag("ip", ip).field("recursivo", int(recursividad)).field("amplifica", int(amplificacion))
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
```
Este código permite una auditoría rápida y automatizada de servidores DNS expuestos.
