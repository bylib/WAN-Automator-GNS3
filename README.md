# WAN Automator - GNS3

WAN Automator es una aplicación local desarrollada en Python y Streamlit para automatizar la creación de topologías base en GNS3 y generar configuraciones Cisco IOS para escenarios de redes WAN.

El proyecto está orientado a automatización y troubleshooting en temas de enrutamiento avanzado, especialmente OSPF multiárea, BGP, Frame Relay, NAT/PAT, ACLs, VLAN, DHCP y SSH.

---

# Problemática

En laboratorios de redes WAN, la configuración manual de protocolos de enrutamiento avanzado puede ser lenta, repetitiva y propensa a errores.

Además, cuando la conectividad falla, es necesario ejecutar múltiples comandos de verificación y documentar el diagnóstico.

WAN Automator busca reducir ese trabajo manual generando topologías base, configuraciones Cisco IOS y guías de troubleshooting a partir de una petición en lenguaje natural.

---

# Funcionalidades

- Verificación de conexión con GNS3
- Creación automática de proyectos en GNS3
- Creación de topología base con switches y VPCS
- Generación de configuración Cisco IOS para:
  - OSPF multiárea
  - BGP
  - Frame Relay
  - NAT/PAT
  - ACLs
  - VLAN
  - DHCP
  - SSH
- Generación de guía de troubleshooting
- Descarga de configuraciones y guías en `.txt`
- Interpretación opcional con Gemini AI

---

# Requisitos

- Python 3.10 o superior
- GNS3 instalado
- Servidor local de GNS3 activo en:

```text
http://localhost:3080/v2
```

---

# Instalación

Instalar dependencias:

```bash
py -m pip install streamlit requests google-genai
```

O usando `requirements.txt`:

```bash
py -m pip install -r requirements.txt
```

---
# Interfaz

![Main Interface](images/main.png)


# Ejecución

1. Abrir GNS3
2. Verificar que GNS3 responda en:

```text
http://localhost:3080/v2/version
```

3. Ejecutar la app:

```bash
py -m streamlit run app.py
```

4. Abrir en el navegador:

```text
http://localhost:8501
```

---

# Uso

1. Abrir la aplicación
2. Presionar **Verificar GNS3**
3. Escribir una petición, por ejemplo:

```text
Crea una red OSPF con 4 áreas, un servidor web y conexión a WAN
```

4. Presionar **Generar topología en GNS3**
5. Revisar:
   - Configuraciones generadas
   - Guía de troubleshooting
   - Guía de laboratorio
6. Descargar los archivos necesarios

---

# Limitación técnica

La herramienta crea una topología base usando los templates disponibles por defecto en GNS3:

- VPCS
- Ethernet Switch

Si no existen routers Cisco instalados como appliances en GNS3, la app no crea routers reales.

En ese caso, genera las configuraciones Cisco IOS como guía para aplicarlas posteriormente en routers reales, IOSv, IOU u otros appliances compatibles.

---

# Ejemplo de salida

Para una petición WAN con OSPF, la app puede generar:

- Proyecto en GNS3
- WAN-CLOUD
- SW-HQ
- WEB-SERVER
- Switches de sucursal
- PCs VPCS
- Configuración de R1-HQ
- Configuración de routers de sucursal
- Comandos de troubleshooting
- Guía de laboratorio

---

# Comandos de troubleshooting generados

Ejemplos:

```bash
show ip interface brief
show ip ospf neighbor
show ip ospf interface brief
show ip route ospf
show ip bgp summary
show ip nat translations
show ip access-lists
ping 192.168.10.10
traceroute 192.168.10.10
```

---

# Integración con Gemini

La app permite usar Gemini de forma opcional para interpretar peticiones más complejas.

⚠️ La API key no debe subirse a GitHub ni dejarse fija en el código.

---

# Autores

- Maria Daniela Nasayo Palencia
- Oscar Jesith Lancheros Arenas
- Jeimi Franchelli Martinez Silva

Proyecto académico orientado a automatización y troubleshooting en redes WAN utilizando Python, Streamlit y GNS3.
