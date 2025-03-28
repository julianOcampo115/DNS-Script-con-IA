# Documentación del Uso de IA en el Desarrollo del Script de Auditoría DNS "DNS_Script.py"

## 1. Explicación General

En el desarrollo de la aplicación de auditoría DNS, se utilizó Inteligencia Artificial (IA) para generar, refinar y optimizar el código, asegurando buenas prácticas de seguridad y eficiencia. A lo largo del proceso, se realizaron múltiples interacciones con la IA para definir la estructura del script, mejorar funcionalidades y solucionar problemas técnicos.


## 2. Texto Literal de los Prompts y Proceso de Refinamiento
- **2.1 Prompt Inicial: Claridad de la Pregunta/Objetivo**
- El primer prompt estableció el objetivo general del proyecto:

"Necesito desarrollar una aplicación en Python para auditoría de servidores DNS en dos niveles: básico y avanzado. La aplicación debe permitir buscar y verificar IPs con servidores DNS expuestos (nivel básico) e incluir funcionalidades avanzadas como verificación de recursividad, detección de amplificación DNS y soporte para múltiples dominios o paginación (nivel avanzado). Además, quiero integrar Shodan u otra herramienta similar para obtener datos adicionales de red. También me gustaría agregar funciones extra como almacenamiento en InfluxDB, notificaciones en Telegram y generación de reportes para visualizar los resultados en Grafana. ¿Me puedes ayudar con el diseño del código, la implementación y las mejores prácticas de seguridad?"

- Este prompt proporcionó a la IA un contexto claro sobre los requisitos y expectativas del proyecto.

- **2.2 Iteraciones y Refinamientos**

## Prompt Secundario:

"Necesito un script en Python que lea direcciones IP desde un archivo de texto y registre en InfluxDB aquellas que sean vulnerables. La base de datos debe almacenar información sobre si la IP resuelve nombres de dominio, si es recursiva y si permite amplificación. También quiero poder consultar las IPs registradas en los últimos 10 minutos."

## Refinamientos Posteriores:

"Quiero que las IPs que se registran en InfluxDB sean las que provienen de la función leer_ips_reporte(). Actualmente se están usando IPs predefinidas en una lista, pero quiero que sean las del archivo."

"El script debería imprimir los datos obtenidos de InfluxDB para verificar que se están almacenando correctamente."

## 2. Alcance de la Aplicación

Este script tiene como objetivo auditar servidores DNS en busca de vulnerabilidades que podrían ser explotadas en ataques DDoS mediante amplificación. La aplicación:

Lee direcciones IP desde un archivo de texto generado previamente por un escaneo.

Registra en InfluxDB solo aquellas direcciones IP que presentan vulnerabilidades, identificando si resuelven nombres de dominio, si permiten consultas recursivas o si son susceptibles a amplificación.

Consulta los últimos registros en la base de datos para verificar que se están almacenando correctamente.

Este código puede ser utilizado en auditorías de seguridad de redes, permitiendo identificar servidores DNS mal configurados y tomar medidas correctivas.

