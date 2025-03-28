import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# 🔹 Configurar conexión a InfluxDB 2.x
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "XXXXXXXXXXXXXXXXXXXXXX"
INFLUXDB_ORG = "UAO"
INFLUXDB_BUCKET = "dns_security"

# 🔹 Inicializar cliente
write_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# 🔹 Enviar datos de prueba
for value in range(5):
    point = (
        Point("measurement1")  # Nombre de la medición
        .tag("tagname1", "tagvalue1")
        .field("field1", value)
    )
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
    print(f"📡 Escribiendo punto {value} en InfluxDB")
    time.sleep(1)

print("✅ Datos escritos en InfluxDB con éxito.")
write_client.close()


# 🔹 Consulta Flux para obtener los datos
# 🔹 Inicializar cliente
client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()

# 🔹 Consulta Flux para obtener los datos
query = """
from(bucket: "dns_security")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
"""

# 🔹 Ejecutar la consulta
tables = query_api.query(query, org=INFLUXDB_ORG)

# 🔹 Imprimir los resultados
for table in tables:
    for record in table.records:
        print(f"📡 Tiempo: {record.get_time()}, Valor: {record.get_value()}")



# 🔹 Cerrar conexión
client.close()
