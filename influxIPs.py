import os
import time
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# 🔹 Configuración de InfluxDB
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
INFLUXDB_ORG = "UAO"
INFLUXDB_BUCKET = "dns_security"

# 🔹 Inicializar cliente de InfluxDB (solo una vez)
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


def registrar_ip_en_influx(ip, resolucion, recursividad, amplificacion):
    """Registra en InfluxDB una IP vulnerable con detalles."""
    point = Point("dns_vulnerable") \
        .tag("ip", ip) \
        .field("resuelve", int(resolucion)) \
        .field("recursivo", int(recursividad)) \
        .field("amplifica", int(amplificacion))

    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
    print(f"✅ IP {ip} registrada en InfluxDB.")


# 🔹 Simulación de detección de IPs vulnerables
ips_detectadas = [
    ("192.168.1.1", True, False, True),
    ("192.168.1.2", False, True, False),
    ("192.168.1.3", True, True, True),
]

for ip, resolvio, recursivo, amplifica in ips_detectadas:
    if recursivo or amplifica:  # Solo registrar si es vulnerable
        registrar_ip_en_influx(ip, resolvio, recursivo, amplifica)

# 🔹 Consulta de datos en InfluxDB (últimos 10 minutos)
query = f"""
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "dns_vulnerable")
"""

tables = query_api.query(query, org=INFLUXDB_ORG)

print("\n📡 Resultados en InfluxDB:")
for table in tables:
    for record in table.records:
        print(f"Tiempo: {record.get_time()}, IP: {record.values['ip']}, "
              f"Resuelve: {record.values['_value']}")


# 🔹 Cerrar conexión al final
client.close()
