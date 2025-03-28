import shodan
import dns.resolver
import socket
import requests

import os
import time
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Configurar la API Key de Shodan
SHODAN_API_KEY = "OscSR1MKM2fICcN5KgVBBJIGnXwrIt8z"
api = shodan.Shodan(SHODAN_API_KEY)

# Configurar Telegram
TELEGRAM_BOT_TOKEN = "7720656194:AAGRh7hySVMNN36O2IcTl6cJa5vNa-0Sbws"
CHAT_ID = "1574894198"

# Archivos de salida
RESULTADOS_FILE = "C:/Users/Julian/Desktop/resultados_dns.txt"
REPORTE_VULNERABLES = "C:/Users/Julian/Desktop/reporte_vulnerables.txt"

def buscar_dns_expuestos():
    """Busca servidores DNS expuestos en Shodan."""
    try:
        resultados = api.search("port:53")
        print(f"Se encontraron {resultados['total']} servidores DNS expuestos.")
        return [match['ip_str'] for match in resultados['matches']]
    except shodan.APIError as e:
        print(f"Error en Shodan: {e}")
        return []

def verificar_resolucion_dns(ip, dominio="google.com"):
    """Verifica si un servidor DNS resuelve un dominio correctamente."""
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]
        respuesta = resolver.resolve(dominio, "A")
        return True, f"{ip} resolvió {dominio} a {', '.join([r.to_text() for r in respuesta])}"
    except Exception:
        return False, f"{ip} no resolvió {dominio}"

def verificar_recursividad(ip):
    """Verifica si el servidor DNS permite recursividad."""
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]
        resolver.use_edns(0, dns.flags.RD)  # Solicitar recursión
        resolver.resolve("example.com", "A")
        return True, f"{ip} es recursivo"
    except dns.resolver.NoAnswer:
        return False, f"{ip} no permite recursión"
    except Exception:
        return False, f"Error verificando recursividad en {ip}"

def detectar_amplificacion(ip):
    """Detecta posible amplificación DNS analizando el tamaño de la respuesta, soportando IPv6."""
    try:
        consulta = b'\x00\x00\x10\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\xFF\x00\x01'
        
        if ":" in ip:
            familia = socket.AF_INET6
        else:
            familia = socket.AF_INET
        
        sock = socket.socket(familia, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(consulta, (ip, 53))
        respuesta, _ = sock.recvfrom(512)
        size = len(respuesta)
        if size > 150:
            return True, f"{ip} responde con {size} bytes [POTENCIAL AMPLIFICACIÓN]"
        else:
            return False, f"{ip} responde con {size} bytes"
    except socket.timeout:
        return False, f"{ip} no respondió."
    except Exception:
        return False, f"Error en {ip} al analizar amplificación."

def enviar_alerta_telegram(ip, resolucion, recursividad, amplificacion):
    """Envía un mensaje de alerta a Telegram si el DNS es inseguro."""
    mensaje = f"🚨 *DNS Inseguro Detectado* 🚨\n"
    mensaje += f"📌 *IP:* {ip}\n"
    
    if resolucion:
        mensaje += f"✅ {resolucion}\n"
    else:
        mensaje += f"❌ {ip} no resolvió google.com\n"
    
    if recursividad:
        mensaje += f"🔄 {recursividad}\n"
    else:
        mensaje += f"🔒 {ip} no permite recursión\n"

    if amplificacion:
        mensaje += f"⚠️ {amplificacion}\n"
    else:
        mensaje += f"🛑 {ip} no mostró signos de amplificación\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

# ===========================
# EJECUCIÓN Y GUARDADO DE RESULTADOS
# ===========================

dns_ips = buscar_dns_expuestos()

with open(RESULTADOS_FILE, "w", encoding="utf-8") as f, open(REPORTE_VULNERABLES, "w", encoding="utf-8") as vuln_f:
    f.write("### Resultados de Auditoría DNS ###\n\n")
    vuln_f.write("### Reporte de Servidores DNS Potencialmente Inseguros ###\n\n")

    for ip in dns_ips[:10]:  # Limitar a 10 IPs para pruebas
        print(f"\n[+] Analizando {ip}")

        resolvio, resultado_resolucion = verificar_resolucion_dns(ip)
        print(resultado_resolucion)

        if not resolvio:
            f.write(f"\n[*] IP: {ip}\n- {resultado_resolucion}\n")
            continue  # Si no responde, no seguimos analizando

        recursivo, resultado_recursividad = verificar_recursividad(ip)
        print(resultado_recursividad)

        amplifica, resultado_amplificacion = detectar_amplificacion(ip)
        print(resultado_amplificacion)

        # Guardar en archivo general
        f.write(f"\n[*] IP: {ip}\n")
        f.write(f"- {resultado_resolucion}\n")
        f.write(f"- {resultado_recursividad}\n")
        f.write(f"- {resultado_amplificacion}\n")

        # Si el servidor es recursivo o amplifica, guardarlo en el reporte de vulnerabilidades
        if recursivo or amplifica:
            vuln_f.write(f"\n[!] IP: {ip}\n")
            vuln_f.write(f"- {resultado_resolucion}\n")
            vuln_f.write(f"- {resultado_recursividad}\n")
            vuln_f.write(f"- {resultado_amplificacion}\n")
            vuln_f.write(f"🚨 **¡Este servidor puede ser explotado!** 🚨\n")

            # 🔹 Enviar alerta de Telegram SOLO si el servidor es inseguro
            enviar_alerta_telegram(ip, resultado_resolucion, resultado_recursividad, resultado_amplificacion)

print(f"\nResultados guardados en '{RESULTADOS_FILE}' 📄✅")
print(f"Reporte de servidores vulnerables en '{REPORTE_VULNERABLES}' 🚨")

def leer_ips_reporte():
    """Lee las IPs desde el archivo de vulnerables y las devuelve en una lista."""
    ips_detectadas = []
    try:
        with open(REPORTE_VULNERABLES, "r", encoding="utf-8") as f:
            for linea in f:
                # Usamos una expresión regular para detectar direcciones IP
                match = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", linea)
                if match:
                    ips_detectadas.append(match.group())
    except FileNotFoundError:
        print(f"⚠️ El archivo '{REPORTE_VULNERABLES}' no existe.")

    return list(set(ips_detectadas))  # Eliminamos duplicados



import requests
from datetime import datetime
import re

ABUSEIPDB_API_KEY = "c6e2e5357df89a36ee5f2d6f7feea3c70b98c21819c14a34b003ac5a3efd9b4e2cc34424bf59f1e8"

def verificar_ip_abuseipdb(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": "365"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    print(f"🔍 Respuesta de la API para {ip}: {response.status_code}")

    if "data" in data:
        abuse_score = data["data"]["abuseConfidenceScore"]
        total_reports = data["data"]["totalReports"]
        last_reported_at = data["data"]["lastReportedAt"]

        if last_reported_at:
            last_reported_at = datetime.strptime(last_reported_at[:10], "%Y-%m-%d").strftime("%d-%b-%Y")
        else:
            last_reported_at = "Nunca"

        resultado = f"\n🔹 **IP Analizada:** {ip}\n"
        resultado += f"   🌍 País: {data['data']['countryCode']}\n"
        resultado += f"   🏢 ISP: {data['data']['isp']}\n"
        resultado += f"   🔗 Dominio: {data['data']['domain']}\n"
        resultado += f"   📡 Uso: {data['data']['usageType']}\n"
        resultado += f"   🕵️ TOR: {'Sí' if data['data']['isTor'] else 'No'}\n"
        resultado += f"   📑 Reportes: {total_reports} ({abuse_score}% de confianza)\n"
        resultado += f"   ⏳ Último reporte: {last_reported_at}\n"

        if abuse_score > 0 or total_reports > 0:
            resultado += "⚠️ *Esta IP ha sido reportada en AbuseIPDB.* ⚠️\n"
            #ip_revisar = ip
            #return ip_revisar
            #print(ip_revisar)
        else:
            resultado += "✅ *Esta IP no ha sido reportada recientemente.* ✅\n"
            #ip_revisar = ip
            #return ip_revisar
            #print(ip_revisar)

        return resultado  # ✅ Ahora siempre se ejecuta
        
    else:
        return f"⚠️ No se pudo obtener información para la IP {ip}. API puede estar limitando la consulta."

# 🔹 Probar con una IP detectada en tu análisis
#ips_a_verificar = ["203.212.241.210", "5.35.244.113"]
ips_a_verificar = leer_ips_reporte()

def enviar_mensaje_telegram(mensaje):
    """Envía un mensaje formateado a Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": resultado, "parse_mode": "Markdown"}
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("📨 Mensaje enviado a Telegram con éxito.")
    else:
        print(f"⚠️ Error al enviar mensaje: {response.text}")

#enviar_mensaje_telegram(resultado)
        

if not ips_a_verificar:
    print("⚠️ No se encontraron IPs en el reporte de vulnerables.")
else:
    for ip in ips_a_verificar:
        resultado = verificar_ip_abuseipdb(ip)
        print(resultado + "\n")
        enviar_mensaje_telegram(resultado)

def enviar_archivo_telegram():
    """Envía el archivo de reporte a Telegram como documento adjunto."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        files = {"document": open(REPORTE_VULNERABLES, "rb")}
        data = {"chat_id": CHAT_ID, "caption": "📄 *Reporte de IPs Vulnerables*"}
        
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("📨 Archivo enviado a Telegram con éxito.")
        else:
            print(f"⚠️ Error al enviar el archivo: {response.text}")
    except FileNotFoundError:
        print(f"⚠️ No se encontró el archivo {REPORTE_VULNERABLES}.")
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")

# Llamar la función
enviar_archivo_telegram()

def enviar_archivo2_telegram():
    """Envía el archivo de reporte a Telegram como documento adjunto."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        files = {"document": open(RESULTADOS_FILE, "rb")}
        data = {"chat_id": CHAT_ID, "caption": "📄 *Reporte de IPs Vulnerables*"}
        
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("📨 Archivo enviado a Telegram con éxito.")
        else:
            print(f"⚠️ Error al enviar el archivo: {response.text}")
    except FileNotFoundError:
        print(f"⚠️ No se encontró el archivo {RESULTADOS_FILE}.")
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")

# Llamar la función
enviar_archivo2_telegram()




#/////////////////////////

import os
import time
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# 🔹 Configuración de InfluxDB
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "XhBJrj8zLEdWWx_nGMt_Mp2jDsqSXGOQ-Eknr2VsaUsz09JNm4ReCkD7cnX0pYtzHD0GETLs3dgUGGQyi0jNOA=="
INFLUXDB_ORG = "UAO"
INFLUXDB_BUCKET = "dns_security"

# 🔹 Inicializar cliente de InfluxDB (solo una vez)
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


def registrar_ip_en_influx(ip, resolucion=False, recursividad=False, amplificacion=False):
    """Registra en InfluxDB una IP vulnerable con detalles."""
    point = Point("dns_vulnerable2") \
        .tag("ip", ip) \
        .field("resuelve", int(resolucion)) \
        .field("recursivo", int(recursividad)) \
        .field("amplifica", int(amplificacion))

    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
    print(f"✅ IP {ip} registrada en InfluxDB con valores -> Resuelve: {resolucion}, Recursivo: {recursividad}, Amplifica: {amplificacion}")


# 🔹 Leer IPs del archivo y registrarlas en InfluxDB


for ip in ips_a_verificar:
    registrar_ip_en_influx(ip)

# 🔹 Consulta de datos en InfluxDB (últimos 10 minutos)
query = f"""
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "dns_vulnerable2")
"""

tables = query_api.query(query, org=INFLUXDB_ORG)

print("\n📡 Resultados en InfluxDB (RAW):")
for table in tables:
    for record in table.records:
        print(f"Tiempo: {record.get_time()}, IP: {record['ip']}, "
              f"Resuelve: {record['_value']}")

# 🔹 Cerrar conexión al final
client.close()


