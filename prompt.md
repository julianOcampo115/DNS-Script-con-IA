Documentación del Uso de IA en el Desarrollo
1. Prompt Utilizado
A continuación, se presenta el conjunto de instrucciones utilizadas para solicitar ayuda en la generación y refinamiento del código con ChatGPT:


Prompt Inicial:
"Necesito desarrollar una aplicación en Python para auditoría de servidores DNS en dos niveles: básico y avanzado. La aplicación debe permitir buscar y verificar IPs con servidores DNS expuestos (nivel básico) e incluir funcionalidades avanzadas como verificación de recursividad, detección de amplificación DNS y soporte para múltiples dominios o paginación (nivel avanzado). Además, quiero integrar Shodan u otra herramienta similar para obtener datos adicionales de red. También me gustaría agregar funciones extra como almacenamiento en InfluxDB, notificaciones en Telegram y generación de reportes para visualizar los resultados en Grafana. ¿Me puedes ayudar con el diseño del código, la implementación y las mejores prácticas de seguridad?"


Prompt Secundario:
"Necesito un script en Python que lea direcciones IP desde un archivo de texto y registre en InfluxDB aquellas que sean vulnerables. La base de datos debe almacenar información sobre si la IP resuelve nombres de dominio, si es recursiva y si permite amplificación. También quiero poder consultar las IPs registradas en los últimos 10 minutos."

Refinamientos Posteriores:

"Quiero que las IPs que se registran en InfluxDB sean las que provienen de la función leer_ips_reporte(). Actualmente se están usando IPs predefinidas en una lista, pero quiero que sean las del archivo."

"El script debería imprimir los datos obtenidos de InfluxDB para verificar que se están almacenando correctamente."

2. Alcance de la Aplicación
Este script tiene como objetivo auditar servidores DNS en busca de vulnerabilidades que podrían ser explotadas en ataques DDoS mediante amplificación. La aplicación:

Lee direcciones IP desde un archivo de texto generado previamente por un escaneo.

Registra en InfluxDB solo aquellas direcciones IP que presentan vulnerabilidades, identificando si resuelven nombres de dominio, si permiten consultas recursivas o si son susceptibles a amplificación.

Consulta los últimos registros en la base de datos para verificar que se están almacenando correctamente.

Este código puede ser utilizado en auditorías de seguridad de redes, permitiendo identificar servidores DNS mal configurados y tomar medidas correctivas.
