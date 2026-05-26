"""
WAN Automator - GNS3  v2.0
Herramienta local para automatizacion, configuracion y troubleshooting WAN.
Mejoras visuales aplicadas: tipografia Sora + JetBrains Mono, paleta dark refinada,
metric cards, tabs mejorados, sidebar con status badge.
"""

import json
import re
from datetime import datetime

import requests
import streamlit as st

try:
    from google import genai
    GEMINI_OK = True
except ImportError:
    GEMINI_OK = False


st.set_page_config(
    page_title="WAN Automator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# ESTILOS VISUALES
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Sora:wght@300;400;500;600;700&display=swap');

:root {
    --bg-base:       #080c14;
    --bg-surface:    #0d1424;
    --bg-card:       #111827;
    --bg-card-hover: #131f35;
    --bg-input:      #0d1424;
    --border:        rgba(56,189,248,0.10);
    --border-hover:  rgba(56,189,248,0.22);
    --accent:        #38bdf8;
    --accent-dim:    rgba(56,189,248,0.08);
    --green:         #34d399;
    --green-dim:     rgba(52,211,153,0.08);
    --amber:         #fbbf24;
    --amber-dim:     rgba(251,191,36,0.08);
    --purple:        #a78bfa;
    --purple-dim:    rgba(167,139,250,0.08);
    --coral:         #fb7185;
    --coral-dim:     rgba(251,113,133,0.08);
    --text-primary:  #e2e8f0;
    --text-muted:    #64748b;
    --text-dim:      #334155;
    --font-ui:       'Sora', sans-serif;
    --font-mono:     'JetBrains Mono', monospace;
    --radius-sm:     6px;
    --radius-md:     10px;
    --radius-lg:     14px;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-ui) !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1180px !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1.4rem 1.1rem !important; }
[data-testid="stSidebar"] .stMarkdown h2 {
    font-family: var(--font-ui) !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    padding-bottom: 0.45rem !important;
    border-bottom: 1px solid var(--border) !important;
    margin-bottom: 0.9rem !important;
}
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: var(--font-ui) !important;
    font-size: 0.63rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

/* BOTONES */
.stButton > button {
    font-family: var(--font-ui) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    border: 1px solid rgba(56,189,248,0.28) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.5rem 1.2rem !important;
    background: rgba(56,189,248,0.05) !important;
    color: var(--accent) !important;
    transition: all 0.16s ease !important;
}
.stButton > button[kind="primary"] {
    background: rgba(56,189,248,0.10) !important;
    border-color: rgba(56,189,248,0.42) !important;
    color: #7dd3fc !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    background: rgba(56,189,248,0.13) !important;
    border-color: rgba(56,189,248,0.52) !important;
    box-shadow: 0 4px 18px rgba(56,189,248,0.11) !important;
}
[data-testid="stDownloadButton"] button {
    background: rgba(52,211,153,0.05) !important;
    border-color: rgba(52,211,153,0.28) !important;
    color: var(--green) !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(52,211,153,0.11) !important;
    border-color: rgba(52,211,153,0.50) !important;
    box-shadow: 0 4px 16px rgba(52,211,153,0.09) !important;
}

/* INPUTS */
.stTextArea textarea,
.stTextInput input,
.stPasswordInput input {
    font-family: var(--font-ui) !important;
    font-size: 0.875rem !important;
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    transition: border-color 0.14s !important;
}
.stTextArea textarea:focus,
.stTextInput input:focus,
.stPasswordInput input:focus {
    border-color: rgba(56,189,248,0.38) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.05) !important;
}
.stTextArea [data-testid="stWidgetLabel"] label,
.stTextInput [data-testid="stWidgetLabel"] label,
.stPasswordInput [data-testid="stWidgetLabel"] label {
    font-family: var(--font-ui) !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.09em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
.stCheckbox label {
    font-family: var(--font-ui) !important;
    font-size: 0.82rem !important;
    color: var(--text-primary) !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 4px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-ui) !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-muted) !important;
    background: transparent !important;
    border: none !important;
    padding: 0.38rem 0.85rem !important;
    transition: all 0.14s !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-dim) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(56,189,248,0.22) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 1.1rem 0 0 !important; }

/* CODE */
.stCode, pre, code { font-family: var(--font-mono) !important; font-size: 0.77rem !important; }
[data-testid="stCode"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    background: #050a10 !important;
}
[data-testid="stCode"] pre { background: transparent !important; }

/* MISC */
hr  { border-color: var(--border) !important; margin: 1.4rem 0 !important; }
h1,h2,h3,h4 { font-family: var(--font-ui) !important; color: var(--text-primary) !important; }
.stAlert,[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    font-family: var(--font-ui) !important;
    font-size: 0.82rem !important;
}
.stCaption,[data-testid="stCaption"] {
    font-family: var(--font-ui) !important;
    font-size: 0.7rem !important;
    color: var(--text-muted) !important;
}

/* ── COMPONENTES CUSTOM ── */

/* Hero */
.wan-hero { padding: 1.6rem 0 1.4rem; border-bottom: 1px solid var(--border); margin-bottom: 1.8rem; }
.wan-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.4rem;
}
.wan-title {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    color: var(--text-primary);
    margin: 0 0 0.3rem;
    line-height: 1.15;
}
.wan-title span { color: var(--accent); }
.wan-sub { font-size: 0.875rem; color: var(--text-muted); margin: 0 0 0.9rem; line-height: 1.55; }
.protocol-pills { display: flex; flex-wrap: wrap; gap: 5px; }
.pill {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid;
}
.p-blue   { background: var(--accent-dim);  color: #7dd3fc; border-color: rgba(56,189,248,0.22); }
.p-green  { background: var(--green-dim);   color: #6ee7b7; border-color: rgba(52,211,153,0.22); }
.p-amber  { background: var(--amber-dim);   color: var(--amber); border-color: rgba(251,191,36,0.22); }
.p-purple { background: var(--purple-dim);  color: var(--purple); border-color: rgba(167,139,250,0.22); }
.p-coral  { background: var(--coral-dim);   color: var(--coral); border-color: rgba(251,113,133,0.22); }

/* GNS3 badge */
.gns3-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    padding: 5px 11px;
    border-radius: 7px;
    border: 1px solid var(--border);
    background: var(--bg-card);
    color: var(--text-muted);
    margin-bottom: 0.9rem;
}
.gns3-badge .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--text-dim); flex-shrink: 0; }
.gns3-badge.online { color: var(--green); border-color: rgba(52,211,153,0.25); background: var(--green-dim); }
.gns3-badge.online .dot { background: var(--green); box-shadow: 0 0 5px var(--green); }

/* Metric cards */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(5,1fr);
    gap: 8px;
    margin-bottom: 1.4rem;
}
.mc {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 14px;
    transition: border-color 0.14s, background 0.14s;
}
.mc:hover { border-color: var(--border-hover); background: var(--bg-card-hover); }
.mc-label {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 7px;
}
.mc-value { font-size: 0.9rem; font-weight: 600; color: var(--text-primary); line-height: 1.2; }
.mc.ab { border-left: 2px solid var(--accent);  }
.mc.ag { border-left: 2px solid var(--green);   }
.mc.ap { border-left: 2px solid var(--purple);  }
.mc.aa { border-left: 2px solid var(--amber);   }

/* Badge */
.badge {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid;
}
.badge-blue   { background: var(--accent-dim);  color: #7dd3fc; border-color: rgba(56,189,248,0.25); }
.badge-green  { background: var(--green-dim);   color: #6ee7b7; border-color: rgba(52,211,153,0.25); }
.badge-orange { background: var(--amber-dim);   color: var(--amber); border-color: rgba(251,191,36,0.25); }
.badge-purple { background: var(--purple-dim);  color: var(--purple); border-color: rgba(167,139,250,0.25); }

/* Config header */
.cfg-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    padding: 10px 14px;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
}
.cfg-title { font-family: var(--font-mono); font-size: 0.8rem; font-weight: 600; color: var(--accent); }
.cfg-meta  { font-family: var(--font-mono); font-size: 0.62rem; color: var(--text-muted); }

/* Section label */
.section-lbl {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 1.4rem 0 0.7rem;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CONSTANTES GNS3
# ─────────────────────────────────────────────────────────────
GNS3_URL     = "http://localhost:3080/v2"
COMPUTE_ID   = "local"
TEMPLATE_VPCS   = "19021f99-e36f-394d-b4a1-8aaa902ab9cc"
TEMPLATE_SWITCH = "1966b864-93e7-32d5-965f-001384eec461"


# ─────────────────────────────────────────────────────────────
# HELPERS GNS3 (sin cambios de logica)
# ─────────────────────────────────────────────────────────────
def gns3(method, path, data=None, timeout=15):
    try:
        r = requests.request(method, f"{GNS3_URL}{path}", json=data, timeout=timeout)
        r.raise_for_status()
        return r.json() if r.text.strip() else {}
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se puede conectar a GNS3. Abre GNS3 y verifica http://localhost:3080/v2/version")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Error GNS3 {r.status_code}: {r.text[:300]}") from e

def verificar_gns3():   return gns3("GET", "/version")
def obtener_templates(): return gns3("GET", "/templates")

def crear_proyecto(nombre):
    return gns3("POST", "/projects", {"name": nombre, "auto_open": True, "auto_start": False})

def crear_nodo(pid, template_id, nombre, x, y):
    return gns3("POST", f"/projects/{pid}/templates/{template_id}",
                {"name": nombre, "x": x, "y": y, "compute_id": COMPUTE_ID})

def crear_link(pid, nodo_a, puerto_a, nodo_b, puerto_b):
    return gns3("POST", f"/projects/{pid}/links", {"nodes": [
        {"node_id": nodo_a["node_id"], "adapter_number": 0, "port_number": puerto_a},
        {"node_id": nodo_b["node_id"], "adapter_number": 0, "port_number": puerto_b}
    ]})

def iniciar_nodo(pid, node_id):
    try: gns3("POST", f"/projects/{pid}/nodes/{node_id}/start")
    except Exception: pass

def resolver_templates(templates_gns3):
    resultado = {"vpcs": TEMPLATE_VPCS, "switch": TEMPLATE_SWITCH}
    for t in templates_gns3:
        nombre = t.get("name","").lower()
        tid    = t.get("template_id","")
        if "vpcs" in nombre and tid:          resultado["vpcs"]   = tid
        if "ethernet switch" in nombre and tid: resultado["switch"] = tid
    return resultado


# ─────────────────────────────────────────────────────────────
# ANALISIS (sin cambios de logica)
# ─────────────────────────────────────────────────────────────
def limpiar_json_respuesta(texto):
    texto = texto.strip()
    for m in ["```json","```"]:
        if texto.startswith(m): texto = texto.replace(m,"",1).strip()
    if texto.endswith("```"): texto = texto[:-3].strip()
    return texto

def detectar_plan_local(texto):
    t = texto.lower()
    pcs = 2
    match_pcs = re.search(r"\b(\d+)\s*(pcs?|computadores?|computadoras?|hosts?|clientes?|equipos?|terminales?)\b", t)
    if match_pcs:
        pcs = max(1, min(int(match_pcs.group(1)), 8))
    else:
        palabras = {"una":1,"un":1,"dos":2,"tres":3,"cuatro":4,"cinco":5,"seis":6,"siete":7,"ocho":8}
        for palabra, numero in palabras.items():
            if re.search(rf"\b{palabra}\s*(pcs?|computadores?|computadoras?|hosts?|clientes?|equipos?)\b", t):
                pcs = numero; break

    vlan_numero = "10"; vlan_nombre = "VENTAS"
    match_vlan = re.search(r"vlan\s*(\d+)", t)
    if match_vlan: vlan_numero = match_vlan.group(1)
    for nombre in ["ventas","admin","administracion","administración","gerencia","invitados","datos","contabilidad","ti"]:
        if nombre in t:
            vlan_nombre = nombre.replace("administración","administracion").upper(); break

    areas = 2
    match_areas = re.search(r"(\d+)\s*(areas?|áreas?)", t)
    if match_areas: areas = max(1, min(int(match_areas.group(1)), 6))
    match_sedes = re.search(r"(\d+)\s*(sucursales?|sedes?|branches?)", t)
    if match_sedes: areas = max(1, min(int(match_sedes.group(1)), 6))

    claves_wan = ["wan","ospf","area","área","areas","áreas","sucursal","sucursales","sede","sedes","isp","bgp","frame relay","frame-relay","mpls","router de borde","servidor web","web server"]
    es_wan = any(c in t for c in claves_wan)

    return {
        "modo": "wan" if es_wan else "lan",
        "pcs": pcs,
        "dhcp": any(c in t for c in ["dhcp","automatica","automática","direcciones auto"]),
        "vlan": "vlan" in t or "ventas" in t or "administracion" in t or "administración" in t,
        "vlan_numero": vlan_numero, "vlan_nombre": vlan_nombre,
        "ssh": "ssh" in t,
        "nat": any(c in t for c in ["nat","internet","salida"]) and "sin nat" not in t,
        "ospf": "ospf" in t or es_wan,
        "areas_ospf": areas,
        "bgp": "bgp" in t or re.search(r"\bas\s+\d+", t) is not None,
        "acl": any(c in t for c in ["acl","filtrado","seguridad","lista de acceso"]),
        "frame_relay": any(c in t for c in ["frame relay","frame-relay"]),
        "servidor_web": any(c in t for c in ["servidor web","web server","http"]),
        "descripcion": "Red detectada localmente"
    }

def analizar_con_gemini(texto, api_key):
    if not GEMINI_OK: raise RuntimeError("Instala google-genai con: py -m pip install google-genai")
    prompt = f"""Eres experto en redes Cisco, WAN, GNS3 y troubleshooting.
Analiza la peticion y devuelve SOLO JSON puro, sin markdown.
Campos requeridos:
{{"modo":"lan"o"wan","pcs":1-8,"dhcp":bool,"vlan":bool,"vlan_numero":"texto","vlan_nombre":"MAYUSCULAS","ssh":bool,"nat":bool,"ospf":bool,"areas_ospf":1-6,"bgp":bool,"acl":bool,"frame_relay":bool,"servidor_web":bool,"descripcion":"resumen"}}
Reglas: OSPF/BGP/WAN/areas/sucursales/ISP/servidor web → modo "wan". Frame Relay → frame_relay true. BGP/AS → bgp true.
Peticion:\n{texto}"""
    cliente = genai.Client(api_key=api_key)
    respuesta = cliente.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    raw = limpiar_json_respuesta(respuesta.text)
    plan = json.loads(raw)
    plan["modo"] = str(plan.get("modo","lan")).lower()
    plan["pcs"]  = max(1, min(int(plan.get("pcs",2)), 8))
    plan["areas_ospf"] = max(1, min(int(plan.get("areas_ospf",2)), 6))
    plan["vlan_numero"] = str(plan.get("vlan_numero","10"))
    plan["vlan_nombre"] = str(plan.get("vlan_nombre","VENTAS")).upper()
    plan["descripcion"] = str(plan.get("descripcion","Red generada con IA"))
    for campo in ["dhcp","vlan","ssh","nat","ospf","bgp","acl","frame_relay","servidor_web"]:
        plan[campo] = bool(plan.get(campo, False))
    return plan


# ─────────────────────────────────────────────────────────────
# GENERADORES DE CONFIG (sin cambios de logica)
# ─────────────────────────────────────────────────────────────
def encabezado(titulo):
    return f"! {'='*58}\n! {titulo}\n! {'='*58}"

def config_router_hq(plan):
    areas = plan.get("areas_ospf",2); usar_nat=plan.get("nat",False)
    usar_bgp=plan.get("bgp",False); usar_acl=plan.get("acl",False); usar_fr=plan.get("frame_relay",False)
    cfg = [encabezado("R1-HQ - Router sede central / Backbone OSPF area 0")]
    cfg.append("""enable
configure terminal
hostname R1-HQ
no ip domain-lookup
ip routing
service password-encryption
banner motd # Acceso restringido - Solo personal autorizado #

interface Loopback0
 description LOOPBACK_ROUTER_ID
 ip address 1.1.1.1 255.255.255.255
 no shutdown

interface GigabitEthernet0/0
 description LAN_HQ_SERVIDORES_192.168.10.0/24
 ip address 192.168.10.1 255.255.255.0
 no shutdown""")
    for i in range(areas):
        sucursal=i+1; ip_hq=f"10.0.{10+sucursal}.1"; interfaz=f"Serial0/0/{i}"; dlci=100+sucursal
        if usar_fr:
            cfg.append(f"\ninterface {interfaz}\n description WAN_FRAME_RELAY_A_SUCURSAL_{sucursal}\n encapsulation frame-relay\n no frame-relay inverse-arp\n frame-relay lmi-type cisco\n no shutdown\n\ninterface {interfaz}.{dlci} point-to-point\n description PVC_A_SUCURSAL_{sucursal}\n ip address {ip_hq} 255.255.255.252\n frame-relay interface-dlci {dlci}")
        else:
            cfg.append(f"\ninterface {interfaz}\n description WAN_A_SUCURSAL_{sucursal}\n ip address {ip_hq} 255.255.255.252\n clock rate 2000000\n no shutdown")
    cfg.append("\nrouter ospf 1\n router-id 1.1.1.1\n network 1.1.1.1 0.0.0.0 area 0\n network 192.168.10.0 0.0.0.255 area 0\n passive-interface GigabitEthernet0/0\n passive-interface Loopback0\n auto-cost reference-bandwidth 1000")
    for i in range(areas):
        cfg.append(f" network 10.0.{11+i}.0 0.0.0.3 area 0")
    if usar_nat:
        cfg.append("""
!
! NAT/PAT
interface GigabitEthernet0/1
 description WAN_HACIA_ISP
 ip address dhcp
 ip nat outside
 no shutdown

interface GigabitEthernet0/0
 ip nat inside

ip access-list standard ACL_NAT_INTERNO
 permit 192.168.10.0 0.0.0.255""")
        for i in range(areas): cfg.append(f" permit 192.168.{20+i}.0 0.0.0.255")
        cfg.append("ip nat inside source list ACL_NAT_INTERNO interface GigabitEthernet0/1 overload\nrouter ospf 1\n default-information originate always")
    if usar_bgp:
        cfg.append("""
!
! BGP hacia ISP
router bgp 65001
 bgp router-id 1.1.1.1
 bgp log-neighbor-changes
 neighbor 203.0.113.1 remote-as 65000
 neighbor 203.0.113.1 description ISP_PROVEEDOR
 address-family ipv4
  network 192.168.10.0 mask 255.255.255.0
  redistribute ospf 1 match internal
  neighbor 203.0.113.1 activate
  neighbor 203.0.113.1 soft-reconfiguration inbound
 exit-address-family""")
    if usar_acl:
        cfg.append("""
!
! ACL WAN
ip access-list extended ACL_WAN_ENTRANTE
 permit tcp any 192.168.10.0 0.0.0.255 eq 80
 permit tcp any 192.168.10.0 0.0.0.255 eq 443
 permit icmp any any echo
 permit icmp any any echo-reply
 deny ip any any log

interface GigabitEthernet0/1
 ip access-group ACL_WAN_ENTRANTE in""")
    cfg.append("\nend\nwrite memory")
    return "\n".join(cfg)

def config_router_branch(plan, area):
    usar_fr=plan.get("frame_relay",False); usar_dhcp=plan.get("dhcp",False)
    usar_vlan=plan.get("vlan",False); usar_ssh=plan.get("ssh",False)
    rnum=area+1; lan_net=f"192.168.{19+area}.0"; lan_gw=f"192.168.{19+area}.1"
    wan_local=f"10.0.{10+area}.2"; wan_remote=f"10.0.{10+area}.1"
    wan_net=f"10.0.{10+area}.0"; dlci=100+area
    cfg = [encabezado(f"R{rnum}-BRANCH - Sucursal {area} / OSPF area {area}")]
    cfg.append(f"""enable
configure terminal
hostname R{rnum}-BRANCH-A{area}
no ip domain-lookup
ip routing
service password-encryption
banner motd # Sucursal {area} - Acceso restringido #

interface Loopback0
 description LOOPBACK_BRANCH_{area}
 ip address {rnum}.{rnum}.{rnum}.{rnum} 255.255.255.255
 no shutdown

interface GigabitEthernet0/0
 description LAN_SUCURSAL_{area}_{lan_net}/24
 ip address {lan_gw} 255.255.255.0
 no shutdown""")
    if usar_dhcp:
        cfg.append(f"\nip dhcp excluded-address {lan_gw}\nip dhcp pool SUCURSAL_{area}_POOL\n network {lan_net} 255.255.255.0\n default-router {lan_gw}\n dns-server 8.8.8.8 8.8.4.4\n lease 1")
    if usar_fr:
        cfg.append(f"\ninterface Serial0/0/0\n description WAN_FRAME_RELAY_A_R1_HQ\n encapsulation frame-relay\n no frame-relay inverse-arp\n frame-relay lmi-type cisco\n no shutdown\n\ninterface Serial0/0/0.{dlci} point-to-point\n description PVC_A_R1_HQ\n ip address {wan_local} 255.255.255.252\n frame-relay interface-dlci {dlci}")
    else:
        cfg.append(f"\ninterface Serial0/0/0\n description WAN_A_R1_HQ\n ip address {wan_local} 255.255.255.252\n no shutdown")
    cfg.append(f"\nrouter ospf 1\n router-id {rnum}.{rnum}.{rnum}.{rnum}\n network {rnum}.{rnum}.{rnum}.{rnum} 0.0.0.0 area {area}\n network {lan_net} 0.0.0.255 area {area}\n network {wan_net} 0.0.0.3 area 0\n passive-interface GigabitEthernet0/0\n passive-interface Loopback0\n area {area} stub\n auto-cost reference-bandwidth 1000\n\nip route 0.0.0.0 0.0.0.0 {wan_remote} 254")
    if usar_vlan:
        vn=plan.get("vlan_numero","10"); vnombre=plan.get("vlan_nombre","VENTAS")
        cfg.append(f"\ninterface GigabitEthernet0/0.{vn}\n description VLAN_{vn}_{vnombre}\n encapsulation dot1Q {vn}\n ip address 192.168.{100+area}.1 255.255.255.0")
    if usar_ssh:
        cfg.append(f"\nip domain-name sucursal{area}.wan.local\ncrypto key generate rsa modulus 2048\nip ssh version 2\nusername admin privilege 15 secret Cisco@WAN{area}\nline vty 0 4\n login local\n transport input ssh\n exec-timeout 15 0")
    cfg.append("\nend\nwrite memory")
    return "\n".join(cfg)

def config_lan_switch(plan):
    usar_vlan=plan.get("vlan",False); vlan_num=plan.get("vlan_numero","10")
    vlan_nombre=plan.get("vlan_nombre","VENTAS"); pcs=plan.get("pcs",2); usar_ssh=plan.get("ssh",False)
    cfg = [encabezado("SW1 - Switch LAN")]
    cfg.append("enable\nconfigure terminal\nhostname SW1\nno ip domain-lookup\nservice password-encryption")
    if usar_vlan:
        cfg.append(f"\nvlan {vlan_num}\n name {vlan_nombre}\nexit\n\ninterface range FastEthernet0/1-{min(pcs,8)}\n description ACCESO_VLAN_{vlan_num}\n switchport mode access\n switchport access vlan {vlan_num}\n spanning-tree portfast\n spanning-tree bpduguard enable\n no shutdown\n\ninterface GigabitEthernet0/1\n description TRUNK_A_ROUTER\n switchport mode trunk\n switchport trunk allowed vlan {vlan_num}\n no shutdown")
    else:
        cfg.append(f"\ninterface range FastEthernet0/1-{min(pcs,8)}\n description ACCESO_LAN\n switchport mode access\n spanning-tree portfast\n spanning-tree bpduguard enable\n no shutdown")
    if usar_ssh:
        cfg.append("\ninterface Vlan1\n ip address 192.168.1.254 255.255.255.0\n no shutdown\nip default-gateway 192.168.1.1\nip domain-name lan.local\ncrypto key generate rsa modulus 1024\nip ssh version 2\nusername admin privilege 15 secret Cisco@Switch\nline vty 0 15\n login local\n transport input ssh")
    cfg.append("\nend\nwrite memory")
    return "\n".join(cfg)

def config_vpcs(plan, modo="wan"):
    lineas = ["! ==================================================","! CONFIGURACION DE VPCS","! =================================================="]
    if modo=="wan":
        areas=plan.get("areas_ospf",2)
        lineas.extend(["","! WEB-SERVER en sede central HQ:","ip 192.168.10.10 255.255.255.0 192.168.10.1","save"])
        for i in range(areas):
            sucursal=i+1; ip=f"192.168.{19+sucursal}.10"; gw=f"192.168.{19+sucursal}.1"
            lineas.extend([f"","! PC-B{sucursal} - Sucursal {sucursal} / Area OSPF {sucursal}:",f"ip {ip} 255.255.255.0 {gw}","save"])
        lineas.extend(["","! Pruebas:","ping 192.168.10.10","trace 192.168.10.10","","! Nota: El ping requiere routers reales/appliances Cisco en GNS3."])
    else:
        pcs=plan.get("pcs",2)
        for i in range(pcs):
            ip=f"192.168.1.{10+i}"
            lineas.extend([f"","! PC{i+1}:","dhcp" if plan.get("dhcp") else f"ip {ip} 255.255.255.0 192.168.1.1","save"])
        lineas.extend(["","! Prueba:","ping 192.168.1.11"])
    return "\n".join(lineas)

def generar_troubleshooting(plan):
    es_wan=plan.get("modo")=="wan" or plan.get("ospf")
    usar_bgp=plan.get("bgp",False); usar_nat=plan.get("nat",False)
    usar_fr=plan.get("frame_relay",False); usar_acl=plan.get("acl",False); areas=plan.get("areas_ospf",2)
    lineas = ["! ==================================================","! GUIA DE TROUBLESHOOTING WAN","! ==================================================","","! 1. Verificar interfaces","show ip interface brief","show interfaces description","show interfaces serial 0/0/0","","! Si aparece administratively down, falta no shutdown.",""]
    if es_wan:
        lineas.extend(["! 2. Verificar OSPF","show ip ospf neighbor","show ip ospf interface brief","show ip ospf database","show ip ospf","","! Estado esperado de vecinos: FULL","","! 3. Verificar rutas","show ip route","show ip route ospf",f"! Deben aparecer rutas OSPF hacia 192.168.10.0 y 192.168.20.0 hasta 192.168.{19+areas}.0","","! Problemas comunes OSPF:","! - Area incorrecta","! - Wildcard mal escrita","! - Interfaces apagadas","! - Router-id duplicado","! - Mascara WAN /30 incorrecta",""])
    if usar_fr: lineas.extend(["! 4. Frame Relay","show frame-relay pvc","show frame-relay map","show frame-relay lmi","","! Estado esperado de PVC: ACTIVE",""])
    if usar_bgp: lineas.extend(["! 5. BGP","show ip bgp summary","show ip bgp","show ip bgp neighbors","","! Si Idle: revisar AS remoto, IP neighbor y conectividad.",""])
    if usar_nat: lineas.extend(["! 6. NAT/PAT","show ip nat translations","show ip nat statistics","debug ip nat","clear ip nat translation *","","! Revisar ip nat inside/outside, ACL de NAT y ruta por defecto.",""])
    if usar_acl: lineas.extend(["! 7. ACLs","show ip access-lists","show ip interface GigabitEthernet0/1","","! Revisar orden de reglas y deny any implicito.",""])
    lineas.extend(["! 8. Pruebas de conectividad","ping 192.168.10.10","ping 192.168.10.10 source loopback0","traceroute 192.168.10.10","","! Checklist:","! [ ] Interfaces UP/UP","! [ ] Vecinos OSPF en FULL","! [ ] Rutas OSPF presentes","! [ ] PCs/VPCS con IP y gateway correctos","! [ ] NAT funcionando si aplica","! [ ] ACLs no bloquean trafico esperado"])
    return "\n".join(lineas)

def generar_guia_lab(plan, topologia):
    es_wan=plan.get("modo")=="wan" or plan.get("ospf"); areas=plan.get("areas_ospf",2)
    desc=plan.get("descripcion","Laboratorio WAN"); nombre=topologia.get("nombre_proyecto","Proyecto WAN")
    lineas = ["==================================================",f"GUIA DE LABORATORIO - {desc.upper()}",f"Proyecto GNS3: {nombre}","==================================================",""]
    if es_wan:
        lineas.extend(["TOPOLOGIA BASE GENERADA EN GNS3:","- WEB-SERVER: VPCS simulando servidor en la red HQ","- SW-HQ: switch de la sede central",f"- {areas} switches de sucursal",f"- {areas} PCs VPCS de sucursal","","CONFIGURACION WAN GENERADA COMO GUIA:","- R1-HQ: router sede central / backbone OSPF area 0"])
        for i in range(areas): lineas.append(f"- R{i+2}-BRANCH: router sucursal {i+1} / area OSPF {i+1}")
        lineas.extend(["","IMPORTANTE:","La app crea switches y VPCS porque tu GNS3 aun no tiene templates de routers Cisco instalados.","Las configuraciones de routers se generan para aplicarlas cuando agregues appliances Cisco a GNS3.","","PLAN DE DIRECCIONAMIENTO:","HQ: 192.168.10.0/24 - WEB-SERVER: 192.168.10.10 - Gateway: 192.168.10.1"])
        for i in range(areas): lineas.append(f"Sucursal {i+1}: LAN 192.168.{20+i}.0/24 - WAN 10.0.{11+i}.0/30")
        lineas.extend(["","PASOS:","1. Revisa la topologia base creada en GNS3.","2. Configura WEB-SERVER y PCs con los comandos VPCS.","3. Cuando tengas routers Cisco/appliances, pega las configs generadas en cada router.","4. Verifica OSPF con show ip ospf neighbor.","5. Prueba conectividad hacia 192.168.10.10."])
    else:
        pcs=plan.get("pcs",2)
        lineas.extend(["TOPOLOGIA LAN GENERADA:","- 1 switch SW1",f"- {pcs} PCs VPCS","","PLAN DE DIRECCIONAMIENTO:"])
        for i in range(pcs): lineas.append(f"PC{i+1}: 192.168.1.{10+i}/24")
        lineas.extend(["","PASOS:","1. Abre consola de cada VPCS.","2. Configura IP segun la pestaña VPCS.","3. Prueba ping entre PCs."])
    if plan.get("nat"): lineas.extend(["","NOTA SOBRE NAT:","La configuracion NAT es valida para Cisco IOS.","En GNS3 local, NAT real puede requerir Cloud, GNS3 VM, VMware o appliance de router."])
    return "\n".join(lineas)

def crear_topologia_wan(plan, pid, templates):
    areas=plan.get("areas_ospf",2); tid_vpcs=templates.get("vpcs",TEMPLATE_VPCS); tid_sw=templates.get("switch",TEMPLATE_SWITCH)
    resultado={"switches":[],"pcs":[],"links":[]}
    hq_x=0; hq_y=-260
    sw_hq    = crear_nodo(pid,tid_sw,"SW-HQ",hq_x,hq_y+170)
    web_server=crear_nodo(pid,tid_vpcs,"WEB-SERVER",hq_x,hq_y+320)
    wan_cloud =crear_nodo(pid,tid_sw,"WAN-CLOUD",hq_x,hq_y+20)
    for n in [sw_hq,web_server,wan_cloud]: iniciar_nodo(pid,n["node_id"])
    crear_link(pid,sw_hq,0,web_server,0)
    crear_link(pid,wan_cloud,0,sw_hq,1)
    resultado["switches"].extend([wan_cloud,sw_hq]); resultado["pcs"].append(web_server)
    branches=[]; sep_x=360; total_w=(areas-1)*sep_x; start_x=-(total_w//2)
    for i in range(areas):
        sucursal=i+1; bx=start_x+i*sep_x; by=220
        sw_b=crear_nodo(pid,tid_sw,f"SW-B{sucursal}",bx,by+120)
        pc_b=crear_nodo(pid,tid_vpcs,f"PC-B{sucursal}",bx,by+270)
        for n in [sw_b,pc_b]: iniciar_nodo(pid,n["node_id"])
        crear_link(pid,sw_b,0,pc_b,0); crear_link(pid,wan_cloud,sucursal,sw_b,1)
        resultado["switches"].append(sw_b); resultado["pcs"].append(pc_b)
        branches.append({"area":sucursal,"sw":sw_b,"pc":pc_b,"x":bx,"y":by})
    return resultado, branches, sw_hq, web_server

def crear_topologia_lan(plan, pid, templates):
    pcs=plan.get("pcs",2); tid_vpcs=templates.get("vpcs",TEMPLATE_VPCS); tid_sw=templates.get("switch",TEMPLATE_SWITCH)
    sw1=crear_nodo(pid,tid_sw,"SW1",0,0); iniciar_nodo(pid,sw1["node_id"])
    sep=180; inicio_x=-((pcs-1)*sep)//2; pcs_nodes=[]
    for i in range(pcs):
        pc=crear_nodo(pid,tid_vpcs,f"PC{i+1}",inicio_x+i*sep,200)
        iniciar_nodo(pid,pc["node_id"]); crear_link(pid,sw1,i,pc,0); pcs_nodes.append(pc)
    return {"switch":sw1,"pcs":pcs_nodes}


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Configuración")

    if "gns3_ok" not in st.session_state:
        st.session_state["gns3_ok"] = False

    # Status badge
    if st.session_state["gns3_ok"]:
        st.markdown('<div class="gns3-badge online"><span class="dot"></span>GNS3 conectado</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="gns3-badge"><span class="dot"></span>GNS3 desconectado</div>', unsafe_allow_html=True)

    st.markdown("### Conexión GNS3")
    st.code(GNS3_URL, language=None)

    if st.button("Verificar GNS3", use_container_width=True):
        try:
            version = verificar_gns3()
            st.session_state["gns3_ok"] = True
            st.success(f"Conectado — v{version.get('version','OK')}")
        except Exception as error:
            st.session_state["gns3_ok"] = False
            st.error("No se pudo conectar a GNS3")
            st.caption(str(error))

    st.divider()
    st.markdown("### Gemini AI")

    api_key = st.text_input("API Key Gemini (opcional)", type="password",
                            help="Mejora la interpretación de peticiones complejas.")

    usar_gemini = st.checkbox("Usar Gemini", value=False, disabled=not GEMINI_OK)
    if not GEMINI_OK:
        st.caption("Instala con: py -m pip install google-genai")

    st.divider()
    st.caption("Mantén GNS3 abierto antes de crear una topología.")
    st.caption("Sin routers Cisco instalados, la app crea la base física con switches y VPCS, y genera las configs WAN como guía.")


# ─────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="wan-hero">
    <div class="wan-eyebrow">// GNS3 Network Automation</div>
    <h1 class="wan-title">WAN <span>Automator</span></h1>
    <p class="wan-sub">Automatización y troubleshooting WAN para GNS3 &mdash;
    genera topologías base, configuraciones Cisco IOS y guías de diagnóstico con un solo prompt.</p>
    <div class="protocol-pills">
        <span class="pill p-blue">OSPF</span>
        <span class="pill p-green">BGP</span>
        <span class="pill p-amber">Frame Relay</span>
        <span class="pill p-blue">NAT / PAT</span>
        <span class="pill p-purple">ACLs</span>
        <span class="pill p-coral">SSH</span>
        <span class="pill p-green">DHCP</span>
        <span class="pill p-amber">VLAN</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# INPUT Y ACCIONES
# ─────────────────────────────────────────────────────────────
preset   = st.session_state.pop("preset", "")
peticion = st.text_area(
    "¿Qué red deseas construir?",
    value=preset,
    placeholder="Ej: Crea una red OSPF con 4 áreas, un servidor web y conexión a WAN",
    height=110
)

col_btn_1, col_btn_2 = st.columns([4, 1])

with col_btn_1:
    if st.session_state.get("gns3_ok", False):
        ejecutar = st.button("Generar topología en GNS3", type="primary", use_container_width=True)
    else:
        st.warning("Primero verifica que GNS3 esté encendido desde el panel lateral.")
        ejecutar = False

with col_btn_2:
    if st.button("Limpiar", use_container_width=True):
        st.session_state.pop("resultado", None)
        st.rerun()


# ─────────────────────────────────────────────────────────────
# EJECUCION
# ─────────────────────────────────────────────────────────────
if ejecutar:
    if not peticion.strip():
        st.warning("Escribe primero qué red deseas crear.")
    else:
        with st.spinner("Analizando petición..."):
            plan = None
            if usar_gemini and api_key:
                try:
                    plan = analizar_con_gemini(peticion, api_key)
                    st.info("Gemini interpretó la petición.")
                except Exception as error:
                    st.warning(f"Gemini falló. Usando detección local. Detalle: {error}")
            if plan is None:
                plan = detectar_plan_local(peticion)

        es_wan = plan.get("modo") == "wan" or plan.get("ospf")

        with st.spinner("Creando topología en GNS3..."):
            try:
                verificar_gns3()
                templates = resolver_templates(obtener_templates())
                nombre_proyecto = f"WAN_{'OSPF' if es_wan else 'LAN'}_{datetime.now().strftime('%H%M%S')}"
                proyecto = crear_proyecto(nombre_proyecto)
                pid = proyecto["project_id"]

                advertencias = []
                topologia_info = {"nombre_proyecto": nombre_proyecto, "tipo": "wan" if es_wan else "lan"}

                if es_wan:
                    resultado_topo, branches, sw_hq, web_server = crear_topologia_wan(plan, pid, templates)
                    topologia_info.update({"areas": plan.get("areas_ospf",2), "sw_hq": sw_hq, "web_server": web_server, "branches": branches})
                    advertencias.append("La topología física usa switches y VPCS porque no hay routers Cisco instalados. Las configs WAN se generan para aplicarlas en routers reales o appliances de GNS3.")
                else:
                    resultado_topo = crear_topologia_lan(plan, pid, templates)

                if plan.get("nat"):
                    advertencias.append("NAT configurado como guía Cisco IOS. Para NAT real en GNS3 local puede requerirse Cloud, GNS3 VM o appliance.")

                configs = []
                if es_wan:
                    configs.append(("R1-HQ", config_router_hq(plan)))
                    for i in range(plan.get("areas_ospf",2)):
                        sucursal = i+1
                        configs.append((f"R{sucursal+1}-BRANCH-A{sucursal}", config_router_branch(plan, sucursal)))
                    configs.append(("VPCS", config_vpcs(plan, "wan")))
                else:
                    configs.append(("SW1", config_lan_switch(plan)))
                    configs.append(("VPCS", config_vpcs(plan, "lan")))

                troubleshooting = generar_troubleshooting(plan)
                guia = generar_guia_lab(plan, topologia_info)

                st.session_state["resultado"] = {
                    "plan": plan, "proyecto": proyecto, "configs": configs,
                    "troubleshooting": troubleshooting, "guia": guia,
                    "advertencias": advertencias, "es_wan": es_wan,
                    "topologia_info": topologia_info, "peticion": peticion
                }
                st.success(f"✓ Topología creada — Proyecto: {nombre_proyecto}")

            except RuntimeError as error:
                st.error(str(error))
            except Exception as error:
                st.error(f"Error inesperado: {error}")
                import traceback
                with st.expander("Ver detalle"):
                    st.code(traceback.format_exc())


# ─────────────────────────────────────────────────────────────
# RESULTADOS
# ─────────────────────────────────────────────────────────────
if "resultado" in st.session_state:
    resultado = st.session_state["resultado"]
    plan      = resultado["plan"]
    es_wan    = resultado["es_wan"]

    st.markdown("---")

    for advertencia in resultado["advertencias"]:
        st.warning(advertencia)

    # ── METRIC CARDS ──
    modo_label  = "WAN multiárea" if es_wan else "LAN"
    modo_accent = "ab" if es_wan else "ag"
    badge_cls   = "badge-blue" if es_wan else "badge-green"
    topo_val    = f'{plan.get("areas_ospf",1)} áreas OSPF' if es_wan else f'{plan.get("pcs",2)} PCs'
    protos      = [e for e, k in [("OSPF","ospf"),("BGP","bgp"),("FR","frame_relay"),("NAT","nat"),("ACL","acl"),("SSH","ssh"),("DHCP","dhcp"),("VLAN","vlan")] if plan.get(k)]
    proto_str   = " · ".join(protos) if protos else "Base"
    nombre_proj = resultado["proyecto"].get("name","—")

    st.markdown(f"""
<div class="section-lbl">Resumen del proyecto</div>
<div class="metrics-grid">
    <div class="mc {modo_accent}">
        <div class="mc-label">Modo</div>
        <div class="mc-value"><span class="badge {badge_cls}">{modo_label}</span></div>
    </div>
    <div class="mc ab">
        <div class="mc-label">Proyecto GNS3</div>
        <div class="mc-value" style="font-size:0.76rem;word-break:break-all">{nombre_proj}</div>
    </div>
    <div class="mc">
        <div class="mc-label">Topología</div>
        <div class="mc-value">{topo_val}</div>
    </div>
    <div class="mc ap">
        <div class="mc-label">Protocolos</div>
        <div class="mc-value" style="font-size:0.72rem;color:var(--text-muted)">{proto_str}</div>
    </div>
    <div class="mc ag">
        <div class="mc-label">Configs generadas</div>
        <div class="mc-value">{len(resultado["configs"])}</div>
    </div>
</div>
""", unsafe_allow_html=True)

    if usar_gemini and api_key:
        with st.expander("Ver interpretación Gemini"):
            st.json(plan)

    # ── TABS ──
    tab_names = [f"⚙ {nombre}" for nombre, _ in resultado["configs"]]
    tab_names += ["🔍 Troubleshooting", "📋 Guía de laboratorio", "⬇ Descargas"]

    tabs = st.tabs(tab_names)

    for idx, (nombre, config) in enumerate(resultado["configs"]):
        with tabs[idx]:
            lineas = len(config.splitlines())
            st.markdown(f"""
<div class="cfg-header">
    <span class="cfg-title">// {nombre}</span>
    <span class="cfg-meta">{lineas} líneas</span>
</div>""", unsafe_allow_html=True)
            st.code(config, language="text")
            st.download_button(
                f"Descargar {nombre}",
                data=config,
                file_name=f"config_{nombre.lower().replace(' ','_')}.txt",
                mime="text/plain",
                key=f"dl_cfg_{idx}"
            )

    with tabs[len(resultado["configs"])]:
        st.markdown('<div class="cfg-header"><span class="cfg-title">// Comandos de verificación y diagnóstico</span></div>', unsafe_allow_html=True)
        st.code(resultado["troubleshooting"], language="text")

    with tabs[len(resultado["configs"]) + 1]:
        st.markdown('<div class="cfg-header"><span class="cfg-title">// Guía paso a paso</span></div>', unsafe_allow_html=True)
        st.code(resultado["guia"], language="text")

    with tabs[len(resultado["configs"]) + 2]:
        st.markdown('<div class="section-lbl">Exportar configuraciones</div>', unsafe_allow_html=True)

        config_completa = "\n\n".join([f"! ===== {n} =====\n{c}" for n,c in resultado["configs"]])
        todo = config_completa + "\n\n" + "="*60 + "\n\n" + resultado["troubleshooting"] + "\n\n" + "="*60 + "\n\n" + resultado["guia"]

        st.download_button(
            "Descargar TODO (configs + troubleshooting + guía)",
            data=todo,
            file_name=f"WAN_Automator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button("Solo configuraciones", data=config_completa, file_name="configs_cisco.txt", mime="text/plain", use_container_width=True)
        with col_d2:
            st.download_button("Solo troubleshooting", data=resultado["troubleshooting"], file_name="troubleshooting_wan.txt", mime="text/plain", use_container_width=True)