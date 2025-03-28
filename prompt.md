# Documentación del Uso de IA en el Desarrollo del Script de Auditoría DNS "DNS_Script.py"

## 1. Explicación General

En el desarrollo de la aplicación de auditoría DNS, se utilizó Inteligencia Artificial (IA) para generar, refinar y optimizar el código, asegurando buenas prácticas de seguridad y eficiencia. A lo largo del proceso, se realizaron múltiples interacciones con la IA para definir la estructura del script, mejorar funcionalidades y solucionar problemas técnicos.


## 2. Texto Literal de los Prompts y Proceso de Refinamiento
- **2.1 Prompt Inicial: Claridad de la Pregunta/Objetivo**
- El primer prompt estableció el objetivo general del proyecto:

"Necesito desarrollar una aplicación en Python para auditoría de servidores DNS en dos niveles: básico y avanzado. La aplicación debe permitir buscar y verificar IPs con servidores DNS expuestos (nivel básico) e incluir funcionalidades avanzadas como verificación de recursividad, detección de amplificación DNS y soporte para múltiples dominios o paginación (nivel avanzado). Además, quiero integrar Shodan u otra herramienta similar para obtener datos adicionales de red. También me gustaría agregar funciones extra como almacenamiento en InfluxDB, notificaciones en Telegram y generación de reportes para visualizar los resultados en Grafana. ¿Me puedes ayudar con el diseño del código, la implementación y las mejores prácticas de seguridad?"

- Este prompt proporcionó a la IA un contexto claro sobre los requisitos y expectativas del proyecto.

- **2.2 Iteraciones y Refinamientos**

Durante el desarrollo, se realizaron ajustes en los prompts para mejorar el código y solucionar problemas específicos:

## Ejemplo 1: Integración con InfluxDB

Prompt de refinamiento:

"Necesito un script en Python que lea direcciones IP desde un archivo de texto y registre en InfluxDB aquellas que sean vulnerables. La base de datos debe almacenar información sobre si la IP resuelve nombres de dominio, si es recursiva y si permite amplificación. También quiero poder consultar las IPs registradas en los últimos 10 minutos."

- Motivo del ajuste: Se especificó cómo debía manejarse la base de datos para almacenar únicamente IPs vulnerables y realizar consultas con filtros de tiempo.

## Ejemplo 2: Corrección en la fuente de IPs analizadas

Prompt de refinamiento:

"Quiero que las IPs que se registran en InfluxDB sean las que provienen de la función leer_ips_reporte(). Actualmente se están usando IPs predefinidas en una lista, pero quiero que sean las del archivo."

- Motivo del ajuste: Se corrigió la fuente de datos para garantizar que el script procesara correctamente los archivos de IPs generados en escaneos previos.

## Ejemplo 3: Validación del almacenamiento de datos

Prompt de refinamiento:

"El script debería imprimir los datos obtenidos de InfluxDB para verificar que se están almacenando correctamente."

- Motivo del ajuste: Se agregó una verificación de datos para evitar fallos en la integración con la base de datos.

## 3. Resultado: Implementación en el Proyecto

Gracias a los prompts y refinamientos, se logró implementar un script funcional con las siguientes características:

* Escaneo de servidores DNS para detectar vulnerabilidades de recursividad y amplificación.
* Almacenamiento en InfluxDB de las IPs vulnerables con detalles sobre su estado.
* Generación de reportes en archivos .csv y .txt para documentación de hallazgos.
* Notificaciones en Telegram para alertar en tiempo real sobre servidores vulnerables.
* Visualización de datos en Grafana para facilitar el análisis de tendencias.

## Ejemplo de Código Generado a Partir de los Prompts
Aquí se muestra un fragmento de código optimizado con la ayuda de la IA:

```
def registrar_en_influxdb(ip, resolviendo, recursiva, amplificacion):
    data_point = {
        "measurement": "auditoria_dns",
        "tags": {"ip": ip},
        "fields": {
            "resolviendo": int(resolviendo),
            "recursiva": int(recursiva),
            "amplificacion": int(amplificacion)
        }
    }
    influxdb_client.write_points([data_point])
```
- Incorporación al proyecto: Este código fue generado tras ajustar los prompts para mejorar la estructura de almacenamiento en InfluxDB.

## 4. Conclusión

El uso de IA en este desarrollo permitió optimizar la estructura del código, mejorar su eficiencia y detectar errores antes de la implementación final. A través de iteraciones y refinamientos de los prompts, se logró un script robusto con buenas prácticas de seguridad y escalabilidad.
