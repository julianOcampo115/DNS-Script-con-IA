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
