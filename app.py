import streamlit as st
import pandas as pd
import json, os, math, copy

ARCHIVO = "datos_ohana.json"
CARPETA_FOTOS = "fotos"
os.makedirs(CARPETA_FOTOS, exist_ok=True)

# =========================================================
#  DATOS INICIALES (materiales, actividades, máquinas, gastos)
# =========================================================
MATERIALES_RAW = [
    ("ADHESIVO", "Doble cara", "Centímetro", 0, ""),
    ("ADHESIVO", "Masking tape", "Centímetro", 0, ""),
    ("ADHESIVO", "Cinta perra", "Centímetro", 1, ""),
    ("ADHESIVO", "Puntos Foam 100", "Pieza", 0, "$5 planilla"),
    ("ADHESIVO", "Silicon frío", "ML", 0, ""),
    ("ADHESIVO", "Silicon caliente", "Barra", 2, ""),
    ("ADHESIVO", "Pegamento blanco", "ML", 0, ""),
    ("ADHESIVO", "Velcro puntos", "Pieza", 0, ""),
    ("DECORACIÓN", "Globos látex 5\"", "Paquete", 0, ""),
    ("DECORACIÓN", "Globos látex 12\"", "Paquete", 0, ""),
    ("DECORACIÓN", "Globos látex largos", "Paquete", 0, ""),
    ("DECORACIÓN", "Globos látex metálicos 5\"", "Paquete", 0, ""),
    ("DECORACIÓN", "Globos látex metálicos 12\"", "Paquete", 0, ""),
    ("DECORACIÓN", "Globo burbuja G", "Pieza", 0, ""),
    ("DECORACIÓN", "Globo burbuja M", "Pieza", 0, ""),
    ("DECORACIÓN", "Gas helio burbuja grande", "Pieza", 96, "7-8 por tanque, tanque $750"),
    ("DECORACIÓN", "Gas helio globo metálico", "Pieza", 35, "20 por tanque, tanque $750"),
    ("DECORACIÓN", "Cordón algodón colores", "Metro", 4, ""),
    ("DECORACIÓN", "Cordón algodón natural", "Metro", 2, ""),
    ("DECORACIÓN", "Cordón yute", "Metro", 1, ""),
    ("DECORACIÓN", "Listón satinado 10mm", "Metro", 2, "rollo 25m"),
    ("DECORACIÓN", "Listón satinado 16mm", "Metro", 2, "rollo 20m"),
    ("DECORACIÓN", "Listón satinado 23mm", "Metro", 4, "rollo 10m"),
    ("DECORACIÓN", "Listón satinado 38mm", "Metro", 6, "rollo 10m"),
    ("DECORACIÓN", "Listón popotillo 10mm", "Metro", 2, "rollo 15m"),
    ("DECORACIÓN", "Listón popotillo 16mm", "Metro", 4, "rollo 15m"),
    ("DECORACIÓN", "Listón popotillo 23mm", "Metro", 5, "rollo 10m"),
    ("DECORACIÓN", "Listón popotillo 38mm", "Metro", 8, "rollo 10m"),
    ("DECORACIÓN", "Listón organza 16mm", "Metro", 2, "rollo 20m"),
    ("DECORACIÓN", "Listón organza 22mm", "Metro", 2, "rollo 20m"),
    ("DECORACIÓN", "Listón organza 38mm", "Metro", 0, ""),
    ("EMBALAJE", "Papel china", "Pliego", 1, "paquete"),
    ("EMBALAJE", "Bolsa non woven mini", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa non woven S", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa non woven M", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa non woven G", "Pieza", 0, ""),
    ("EMBALAJE", "Caja cartón IKEA", "Pieza", 15, ""),
    ("EMBALAJE", "Stickers", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa celofán adhesivo", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa celofán papas", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa celofán playeras", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa celofán tags", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa plástico dulces", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa plástico palomitas", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa kraft", "Pieza", 0, ""),
    ("EMBALAJE", "Bolsa celofán cake toppers", "Pieza", 0, ""),
    ("EMBALAJE", "Hoja espuma", "Lienzo", 0, ""),
    ("EMBALAJE", "Cartón base", "Hoja", 0, ""),
    ("HERRAJES", "Eyelets", "Pieza", 0, ""),
    ("HERRAJES", "Argollas colores 8mm", "Pieza", 0, ""),
    ("HERRAJES", "Cadenitas colores", "Pieza", 1, ""),
    ("HERRAJES", "Argollas llavero plata", "Pieza", 0, ""),
    ("HERRAJES", "Argollas llavero Oro", "Pieza", 0, ""),
    ("HERRAJES", "Argollas corazón", "Pieza", 5, ""),
    ("HERRAJES", "Mosquetones colores", "Pieza", 5, ""),
    ("HERRAJES", "Argollas grandes colores", "Pieza", 5, ""),
    ("HERRAJES", "Argollas colores 6mm", "Pieza", 0, ""),
    ("HERRAJES", "Cadenita balines", "Pieza", 1, ""),
    ("HERRAJES", "Imanes 8x1mm", "Pieza", 2, ""),
    ("HERRAJES", "Mini clavitos", "Pieza", 1, ""),
    ("HERRAJES", "Etiquetas equipaje", "Pieza", 0, ""),
    ("HERRAJES", "Cuentas Madera 16mm Nat", "Pieza", 1, ""),
    ("HERRAJES", "Cuentas plástico colores 14mm", "Pieza", 1, ""),
    ("HERRAJES", "Etiquetas rascables rosa", "Pieza", 0, ""),
    ("HERRAJES", "Cuentas madera peques", "Pieza", 0, ""),
    ("HERRAJES", "Cuentas pintadas colores 10mm", "Pieza", 0, ""),
    ("IMPRESIÓN 3D", "PLA", "Gramo", 1, ""),
    ("IMPRESIÓN 3D", "TPU", "Gramo", 0, ""),
    ("IMPRESIONES", "Impresión Bond B/N", "Hoja", 3, "T/C"),
    ("IMPRESIONES", "Impresión fotográfica color", "Hoja", 0, ""),
    ("IMPRESIONES", "Impresión adhesiva", "Hoja", 0, ""),
    ("IMPRESIONES", "Impresión glossy", "Hoja", 0, ""),
    ("IMPRESIONES", "Impresión Bond B/N (tabloide)", "Tabloide", 0, ""),
    ("IMPRESIONES", "Impresión fotográfica color (tabloide)", "Tabloide", 20, "Lumen"),
    ("IMPRESIONES", "Impresión adhesiva (tabloide)", "Tabloide", 18, "Claudio"),
    ("IMPRESIONES", "Impresión glossy (tabloide)", "Tabloide", 15, "Claudio"),
    ("IMPRESIONES", "DTF Textil", "cm2", 0, "Printu 58x100, ref $190"),
    ("IMPRESIONES", "Vinil Adhesivo (plotter)", "ML", 490, ""),
    ("IMPRESIONES", "DTF UV", "cm2", 0, ""),
    ("MATERIALES", "MDF 3mm", "cm2", 0, ""),
    ("MATERIALES", "MDF 6mm", "cm2", 0, ""),
    ("MATERIALES", "Triplay 3mm", "cm2", 0, ""),
    ("MATERIALES", "Caobilla 3mm", "cm2", 0, ""),
    ("MATERIALES", "Acrílico clear 2mm", "cm2", 0, ""),
    ("MATERIALES", "Acrílico clear 3mm", "cm2", 0, ""),
    ("MATERIALES", "Acrílico color 2mm", "cm2", 0, ""),
    ("MATERIALES", "Acrílico color 3mm", "cm2", 1, ""),
    ("MATERIALES", "Acrílico espejo 2mm", "cm2", 0, ""),
    ("MATERIALES", "Acrílico espejo 3mm", "cm2", 0, ""),
    ("MATERIALES", "Acrílico glitter 3mm", "cm2", 0, ""),
    ("MATERIALES", "Bicolam", "cm2", 0, ""),
    ("MATERIALES", "Chapetones par mini", "Pieza", 0, ""),
    ("MATERIALES", "Chapetones chicos", "Pieza", 30, ""),
    ("MATERIALES", "Tira botecitos pintura x6", "Pieza", 2, ""),
    ("MATERIALES", "Crayolas 12", "Caja", 8, ""),
    ("MATERIALES", "Plumones acrílicos Indra 12", "Caja", 38, ""),
    ("MATERIALES", "Plumones acrílicos Indra 24", "Caja", 75, ""),
    ("MATERIALES", "Posavasos corcho adhesivo", "Pieza", 2, ""),
    ("MATERIALES", "Politec 100ml", "ML", 0, "ref venta $25"),
    ("MATERIALES", "Politec 250ml", "ML", 0, "ref venta $50"),
    ("MATERIALES", "Papel Mala IKEA rollo", "cmL", 0.033, "ref venta $100"),
    ("PAPELES", "Cart Color Plus", "Lienzo", 4, "30x59"),
    ("PAPELES", "Cart Opalina", "Lienzo", 4, ""),
    ("PAPELES", "Cart Sirio Pearl", "Lienzo", 16, ""),
    ("PAPELES", "Cart Bristol", "Hoja", 1, "21.5x28"),
    ("PAPELES", "Cartón Gris IKEA", "Cuadro IKEA", 5, "30.5x40.5"),
    ("PAPELES", "Papel Kraft", "Metro", 0, ""),
    ("PAPELES", "Papel Fotográfico", "Hoja", 0, ""),
    ("PAPELES", "Papel Couche adhesivo", "Hoja", 0, ""),
    ("PAPELES", "Papel Glossy", "Hoja", 0, ""),
    ("PAPELES", "Papel acetato", "Lienzo", 0, ""),
    ("PAPELES", "Cart Holográfica", "Lienzo", 0, ""),
    ("PAPELES", "Papel puntitos", "Hoja", 12, ""),
    ("PAPELES", "Cartón gris (hoja)", "Hoja", 0, ""),
    ("PAPELES", "Cartón gris (lienzo)", "Lienzo", 0, ""),
    ("PAPELES", "Cart ilustración blanca", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Vinil adhesivo sencillo", "Lienzo", 22, "30x60"),
    ("PERSONALIZACIÓN", "Vinil adhesivo metálico", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Vinil adhesivo glitter", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Vinil adhesivo cepillado", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Vinil adhesivo Tornasol", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Vinil textil sencillo", "Paquete", 0, ""),
    ("PERSONALIZACIÓN", "Vinil textil detalle", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Vinil textil glitter", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Vinil textil Flocked", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Vinil textil neón", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Vinil textil glow", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Transfer", "Lienzo", 0, ""),
    ("PERSONALIZACIÓN", "Papel para sublimar", "Hoja", 0, ""),
    ("PRODUCTOS BASE", "Playera blanca mujer redondo", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera blanca mujer V", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera negra mujer redondo", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera negra mujer V", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera color mujer redondo", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera color mujer V", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera blanca hombre redondo", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera blanca hombre V", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera negra hombre redondo", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera negra hombre V", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera color hombre redondo", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Playera color hombre V", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Hoodie gorro canguro", "Pieza", 275, ""),
    ("PRODUCTOS BASE", "Hoodie básica", "Pieza", 180, ""),
    ("PRODUCTOS BASE", "Hoodie niño", "Pieza", 190, ""),
    ("PRODUCTOS BASE", "Tote Bag Kit Hangover", "Pieza", 16, ""),
    ("PRODUCTOS BASE", "Tote Bag Grande", "Pieza", 20, ""),
    ("PRODUCTOS BASE", "Costalito jareta manta", "Pieza", 20, ""),
    ("PRODUCTOS BASE", "Cilindro caramelo", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Cilindro Bubble", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Cilindro doble", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Vaso cafetero", "Pieza", 7, ""),
    ("PRODUCTOS BASE", "Cilindro Tipo Stanley", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "Cilindro Skinny metal", "Pieza", 0, ""),
    ("PRODUCTOS BASE", "PlayDoh", "Pieza", 13, ""),
]

ACTIVIDADES_INICIALES = {
    "Diseño": 300, "Corte láser": 120, "Corte cricut": 120, "Depilar vinil": 130,
    "Planchar": 100, "Armar empaques": 100, "Llenar kits": 80,
    "Llenar dulces y sellar": 80, "Refinar cantos": 100, "Pegar cajas MDF": 100,
    "Pegar cajas acrílico": 120, "Lijar": 80, "Etiquetar": 60, "Hacer moños": 60,
    "Pegar vinil": 80, "Armar cuadros": 150, "Imprimir 3D": 80,
    "Imprimir papel": 60, "Embolsar productos": 60,
}

MAQUINAS_INICIALES = {
    "Láser Beri": 19, "Láser X Tool": 29, "Creality (impresora 3D)": 7,
    "X Tool bebé": 8, "Cricut": 4, "Impresora tinta": 2, "Impresora sublimación": 2,
    "Plancha HTV RONT": 3, "Plancha mini": 0, "Selladora": 0, "Crop a Dile": 1,
    "Engargoladora": 2, "Minc": 2, "Laminadora": 2, "Engrapadora larga": 0,
    "Lijadora": 1, "Tanque de helio": 65,
}

GASTOS_FIJOS_INICIALES = {
    "renta": 2000.0, "luz": 200.0, "agua": 200.0, "internet": 300.0,
    "apps": 300.0, "adobe": 500.0, "gasolina": 2500.0, "mantenimiento": 600.0,
    "dominio": 150.0, "dias_mes": 20.0, "horas_dia": 6.0,
}


def construir_datos_iniciales():
    materiales = {}
    for cat, nombre, unidad, costo, nota in MATERIALES_RAW:
        clave, i = nombre, 2
        while clave in materiales:
            clave = f"{nombre} ({i})"; i += 1
        materiales[clave] = {"categoria": cat, "unidad": unidad, "costo": float(costo), "nota": nota}
    return {
        "config": {"moneda": "$", "margen_pct": 40.0, "impuesto_pct": 0.0, "redondeo": 1.0},
        "gastos_fijos": dict(GASTOS_FIJOS_INICIALES),
        "materiales": materiales,
        "actividades": {k: float(v) for k, v in ACTIVIDADES_INICIALES.items()},
        "maquinas": {k: float(v) for k, v in MAQUINAS_INICIALES.items()},
        "productos": {},
    }


def cargar():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
        # Asegura compatibilidad si vienes de una versión anterior
        for p in datos["productos"].values():
            p.setdefault("descripcion", "")
            p.setdefault("categoria", "")
            p.setdefault("foto", "")
            p.setdefault("publicado", False)
        return datos
    datos = construir_datos_iniciales()
    guardar(datos)
    return datos


def guardar(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def calcular_gastos_fijos(datos):
    g = datos["gastos_fijos"]
    conceptos = ["renta", "luz", "agua", "internet", "apps", "adobe", "gasolina", "mantenimiento", "dominio"]
    total_mensual = sum(g[c] for c in conceptos)
    total_horas = g["dias_mes"] * g["horas_dia"]
    costo_hora = total_mensual / total_horas if total_horas else 0
    return total_mensual, total_horas, costo_hora, costo_hora / 60


def calcular(datos, prod):
    cfg = datos["config"]
    _, _, _, costo_min_fijo = calcular_gastos_fijos(datos)

    costo_materiales, detalle_mat = 0.0, []
    for it in prod["materiales"]:
        m = datos["materiales"].get(it["material"])
        cu = m["costo"] if m else 0
        sub = it["cantidad"] * cu
        costo_materiales += sub
        detalle_mat.append((it["material"], it["cantidad"], m["unidad"] if m else "?", sub))

    costo_mano_obra, detalle_act = 0.0, []
    for it in prod["actividades"]:
        ph = datos["actividades"].get(it["actividad"], 0)
        sub = it["minutos"] * (ph / 60)
        costo_mano_obra += sub
        detalle_act.append((it["actividad"], it["minutos"], sub))

    costo_maquinas, detalle_maq = 0.0, []
    for it in prod["maquinas"]:
        ch = datos["maquinas"].get(it["maquina"], 0)
        sub = it["minutos"] * (ch / 60)
        costo_maquinas += sub
        detalle_maq.append((it["maquina"], it["minutos"], sub))

    indirectos = prod["minutos_proceso"] * costo_min_fijo
    otros = prod["otros_costos"]
    costo_total = costo_materiales + costo_mano_obra + costo_maquinas + indirectos + otros
    unidades = max(prod["unidades_lote"], 1)
    costo_unit = costo_total / unidades

    margen = prod["margen_pct"] if prod.get("margen_pct") is not None else cfg["margen_pct"]
    margen = min(margen, 99.9)
    precio = costo_unit / (1 - margen / 100)
    precio_final = precio * (1 + cfg["impuesto_pct"] / 100)
    if cfg["redondeo"] > 0:
        precio_final = math.ceil(precio_final / cfg["redondeo"]) * cfg["redondeo"]

    return dict(detalle_mat=detalle_mat, detalle_act=detalle_act, detalle_maq=detalle_maq,
                costo_materiales=costo_materiales, costo_mano_obra=costo_mano_obra,
                costo_maquinas=costo_maquinas, indirectos=indirectos, otros=otros,
                costo_total=costo_total, costo_unit=costo_unit, margen=margen,
                precio_sin_imp=precio, precio_final=precio_final,
                ganancia=precio_final / (1 + cfg["impuesto_pct"] / 100) - costo_unit)


# =========================================================
#  ESTILO VISUAL OHANA 11:11
# =========================================================
st.set_page_config(page_title="Ohana 11:11 · Costos", page_icon="logo.png", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #E6007E !important; }

.stApp { background: linear-gradient(180deg, #FFEFF7 0%, #FFFFFF 30%); }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E6007E 0%, #B5005F 100%);
}
section[data-testid="stSidebar"] * { color: #FFF8F0 !important; }

div.stButton > button {
    background: #F7941D; color: white; border: none; border-radius: 999px;
    font-weight: 600; padding: 0.5em 1.5em; transition: 0.2s;
}
div.stButton > button:hover { background: #E6007E; color: white; transform: scale(1.03); }

.ohana-card {
    background: white; border-radius: 22px; padding: 1.3em 1.6em;
    box-shadow: 0 6px 18px rgba(230,0,126,0.15); border: 2px solid #FBD6E8;
    margin-bottom: 1.1em;
}
.ohana-badge {
    display:inline-block; background:#FBD6E8; color:#E6007E;
    padding: 4px 14px; border-radius: 999px; font-size:0.78em; font-weight:700;
    margin-right:6px;
}
.price-box {
    background: linear-gradient(135deg, #E6007E, #F7941D);
    border-radius: 24px; padding: 1.6em; text-align:center; color: white;
}
.price-box .label { font-size:0.9em; opacity:0.9; letter-spacing:1px; }
.price-box .value { font-family:'Playfair Display', serif; font-size:2.6em; font-weight:800; }

.catalogo-hero {
    text-align:center; padding: 2em 1em 1em 1em;
}
.catalogo-hero h1 { font-size: 2.8em; margin-bottom:0; }
.catalogo-hero p { color:#B5005F; font-weight:600; }

.btn-whatsapp {
    display:inline-block; background:#25D366; color:white !important; border:0;
    border-radius:999px; padding:10px 22px; font-weight:700; text-decoration:none;
    margin-top: 0.4em;
}
.btn-whatsapp:hover { background:#1DA851; }

hr { border-top: 2px dashed #FBD6E8; }
/* Titulos de las secciones desplegables */
[data-testid="stMain"] [data-testid="stExpander"] summary {
    background-color: #FCE4EF !important;
    border-radius: 12px;
}

/* Texto y flechas de esos titulos */
[data-testid="stMain"] [data-testid="stExpander"] summary,
[data-testid="stMain"] [data-testid="stExpander"] summary * {
    color: #7D1647 !important;
    opacity: 1 !important;
}

/* Etiquetas de los campos del panel principal */
[data-testid="stMain"] [data-testid="stWidgetLabel"],
[data-testid="stMain"] [data-testid="stWidgetLabel"] p {
    color: #333333 !important;
}
/* =====================================================
   CONTROLES PRINCIPALES — ESTILO OHANA
   ===================================================== */

/* Color general del contenido principal */
[data-testid="stAppViewContainer"] {
    color: #3B2433 !important;
}

/* Etiquetas de los campos */
[data-testid="stAppViewContainer"] [data-testid="stWidgetLabel"] *,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] label p {
    color: #6E3154 !important;
    font-weight: 600 !important;
}

/* Campos de texto, números y áreas de texto */
[data-testid="stAppViewContainer"] input,
[data-testid="stAppViewContainer"] textarea {
    background-color: #FFFFFF !important;
    color: #3B2433 !important;
    caret-color: #E6007E !important;
    border: 2px solid #F3B8D2 !important;
    border-radius: 12px !important;
}

/* Contenedores internos de los campos */
[data-testid="stAppViewContainer"] [data-baseweb="input"],
[data-testid="stAppViewContainer"] [data-baseweb="textarea"] {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
}

/* Campo seleccionado */
[data-testid="stAppViewContainer"] input:focus,
[data-testid="stAppViewContainer"] textarea:focus {
    border-color: #E6007E !important;
    box-shadow: 0 0 0 3px rgba(230, 0, 126, 0.15) !important;
    outline: none !important;
}

/* Selectores desplegables */
[data-testid="stAppViewContainer"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #3B2433 !important;
    border: 2px solid #F3B8D2 !important;
    border-radius: 12px !important;
}

/* Texto dentro de los selectores */
[data-testid="stAppViewContainer"] [data-baseweb="select"] span,
[data-testid="stAppViewContainer"] [data-baseweb="select"] div {
    color: #3B2433 !important;
}

/* Menú desplegable */
[data-baseweb="menu"],
[role="listbox"],
[role="option"] {
    background-color: #FFFFFF !important;
    color: #3B2433 !important;
}

[data-baseweb="menu"] *,
[role="listbox"] *,
[role="option"] * {
    color: #3B2433 !important;
}

/* Opción seleccionada en un menú */
[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background-color: #FFE0EF !important;
    color: #B5005F !important;
}

/* Radio buttons */
[data-testid="stRadio"] label,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] span {
    color: #3B2433 !important;
}

[data-testid="stRadio"] input {
    accent-color: #E6007E !important;
}

/* Casillas de selección */
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] label p {
    color: #3B2433 !important;
}

/* Ayudas y textos secundarios */
[data-testid="stAppViewContainer"] small,
[data-testid="stAppViewContainer"] .stCaption {
    color: #8A5270 !important;
}
</style>
""", unsafe_allow_html=True)


def card(html):
    st.markdown(f'<div class="ohana-card">{html}</div>', unsafe_allow_html=True)


NOMBRE_NEGOCIO = st.secrets.get("negocio", {}).get("nombre", "Ohana 11:11")
WHATSAPP_NUM = st.secrets.get("negocio", {}).get("whatsapp", "5215526691918")


def link_whatsapp(producto):
    msg = f"Hola, me interesa cotizar: {producto}"
    msg = msg.replace(" ", "%20")
    return f"https://wa.me/{WHATSAPP_NUM}?text={msg}"


# =========================================================
#  CARGA DE DATOS
# =========================================================
if "datos" not in st.session_state:
    st.session_state["datos"] = cargar()
datos = st.session_state["datos"]


def guardar_estado():
    guardar(datos)


# =========================================================
#  RENDER DE UNA TARJETA DE CATÁLOGO (reutilizable)
# =========================================================
def tarjeta_catalogo(nombre, producto, r):
    st.markdown("<div class='ohana-card'>", unsafe_allow_html=True)
    foto = producto.get("foto", "")
    if foto and os.path.exists(foto):
        st.image(foto, use_container_width=True)
    else:
        st.markdown(
            "<div style='background:#FBD6E8;padding:70px 10px;text-align:center;"
            "border-radius:18px;font-size:50px;'>🌸</div>", unsafe_allow_html=True)

    st.subheader(nombre)
    if producto.get("categoria"):
        st.markdown(f"<span class='ohana-badge'>{producto['categoria']}</span>", unsafe_allow_html=True)
    if producto.get("descripcion"):
        st.write(producto["descripcion"])

    st.markdown(
        f"<h2 style='color:#E6007E;margin-bottom:0;'>Desde ${r['precio_final']:,.2f}</h2>",
        unsafe_allow_html=True)

    st.markdown(
        f'<a class="btn-whatsapp" href="{link_whatsapp(nombre)}" target="_blank">💬 Cotizar por WhatsApp</a>',
        unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def pagina_catalogo_contenido():
    st.markdown(f"""
    <div class="catalogo-hero">
        <h1>✨ {NOMBRE_NEGOCIO} ✨</h1>
        <p>Productos personalizados hechos con mucho cariño 🌸</p>
    </div>
    """, unsafe_allow_html=True)

    productos_publicados = [(n, p) for n, p in datos["productos"].items() if p.get("publicado")]

    if not productos_publicados:
        st.info("Muy pronto encontrarás aquí nuestros productos ✨")
        return

    categorias = sorted(set(p.get("categoria", "General") or "General" for _, p in productos_publicados))
    filtro = st.selectbox("Filtrar por categoría", ["Todas"] + categorias)

    cols = st.columns(3)
    i = 0
    for nombre, producto in productos_publicados:
        cat = producto.get("categoria", "General") or "General"
        if filtro != "Todas" and cat != filtro:
            continue
        r = calcular(datos, producto)
        with cols[i % 3]:
            tarjeta_catalogo(nombre, producto, r)
        i += 1


# =========================================================
#  MODO CATÁLOGO AUTÓNOMO (link para compartir, sin menú)
#  Ejemplo: http://localhost:8501/?catalogo=1
# =========================================================
params = st.query_params
if params.get("catalogo") == "1":
    st.markdown("<style>section[data-testid='stSidebar']{display:none;}</style>", unsafe_allow_html=True)
    pagina_catalogo_contenido()
    st.stop()


# =========================================================
#  LOGIN
# =========================================================
def iniciar_sesion():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    st.sidebar.markdown("## 🔐 Acceso privado")

    if st.session_state.autenticado:
        st.sidebar.success("Sesión iniciada ✔")
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.autenticado = False
            st.rerun()
        return True

    usuario = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        try:
            u_ok = st.secrets["usuarios"]["admin"]["usuario"]
            p_ok = st.secrets["usuarios"]["admin"]["password"]
        except Exception:
            st.sidebar.error("Falta configurar .streamlit/secrets.toml")
            return False
        if usuario == u_ok and password == p_ok:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.sidebar.error("Usuario o contraseña incorrectos")
    return False


# =========================================================
#  SIDEBAR Y MENÚ
# =========================================================
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=120)
    st.markdown(
        f"<h1 style='text-align:center;color:white !important;"
        f"font-family:Playfair Display,serif;'>{NOMBRE_NEGOCIO}</h1>",
        unsafe_allow_html=True)
    st.markdown("---")

sesion = iniciar_sesion()

with st.sidebar:
    st.markdown("---")
    opciones = ["🛍️ Catálogo público"]
    if sesion:
        opciones += [
            "🏠 Inicio", "🧵 Materiales", "🛠️ Mano de obra y Máquinas",
            "🏢 Gastos fijos", "📦 Productos y Servicios",
            "💲 Lista de precios", "⚙️ Configuración",
        ]
    pagina = st.radio("Menú", opciones, label_visibility="collapsed")

    if sesion:
        st.markdown("---")
        link_compartir = "?catalogo=1"
        st.caption("🔗 Link para compartir el catálogo:")
        st.code(link_compartir, language=None)


# =========================================================
#  PÁGINA: CATÁLOGO (dentro del panel normal)
# =========================================================
if pagina == "🛍️ Catálogo público":
    pagina_catalogo_contenido()

elif not sesion:
    st.stop()  # seguridad extra: nada más se muestra sin login

# =========================================================
#  PÁGINA: INICIO
# =========================================================
elif pagina == "🏠 Inicio":
    st.title("Calculadora de Costos · Ohana 11:11")
    st.write("Calcula el costo real de cada producto o servicio y obtén tu precio de venta ideal. ✨")

    total_mat = len(datos["materiales"])
    pendientes = sum(1 for m in datos["materiales"].values() if m["costo"] == 0)
    total_prod = len(datos["productos"])
    publicados = sum(1 for p in datos["productos"].values() if p.get("publicado"))
    _, _, c_hora, c_min = calcular_gastos_fijos(datos)

    c1, c2, c3, c4 = st.columns(4)
    with c1: card(f"<div class='ohana-badge'>MATERIALES</div><h2>{total_mat}</h2>registrados")
    with c2: card(f"<div class='ohana-badge'>PENDIENTES</div><h2>{pendientes}</h2>sin precio ⚠️")
    with c3: card(f"<div class='ohana-badge'>PRODUCTOS</div><h2>{total_prod}</h2>{publicados} en catálogo")
    with c4: card(f"<div class='ohana-badge'>GASTOS FIJOS</div><h2>${c_min:,.2f}</h2>por minuto")

    if pendientes:
        with st.expander(f"⚠️ Ver los {pendientes} materiales sin precio"):
            for n, m in datos["materiales"].items():
                if m["costo"] == 0:
                    st.write(f"- **{n}** ({m['categoria']})")


# =========================================================
#  PÁGINA: MATERIALES
# =========================================================
elif pagina == "🧵 Materiales":
    st.title("🧵 Materiales e insumos")

    categorias = sorted(set(m["categoria"] for m in datos["materiales"].values()))
    filtro = st.selectbox("Filtrar por categoría", ["Todas"] + categorias)

    filas = [{"Material": n, "Categoría": m["categoria"], "Unidad": m["unidad"],
              "Costo": m["costo"], "Nota": m["nota"]}
             for n, m in datos["materiales"].items()
             if filtro == "Todas" or m["categoria"] == filtro]

    if filas:
        df = pd.DataFrame(filas).sort_values(["Categoría", "Material"])

        def resaltar_fila(row):
            if row["Costo"] == 0:
                return ['background-color:#FFD6E8; color:#B5005F; font-weight:600;' for _ in row]
            else:
                return ['background-color:#FFFFFF; color:#333333;' for _ in row]

        st.dataframe(
            df.style.apply(resaltar_fila, axis=1).format({"Costo": "${:,.2f}"}),
            use_container_width=True, hide_index=True, height=420)
    else:
        st.info("No hay materiales en esta categoría.")
    st.markdown("---")
    with st.expander("➕ Agregar o editar material"):
        existentes = sorted(datos["materiales"].keys())
        modo = st.radio("¿Qué quieres hacer?", ["Nuevo material", "Editar uno existente"], horizontal=True)
        if modo == "Editar uno existente" and existentes:
            sel = st.selectbox("Elige el material", existentes)
            actual = datos["materiales"][sel]
        else:
            sel, actual = "", {"categoria": "", "unidad": "", "costo": 0.0, "nota": ""}

        with st.form("form_material"):
            nombre = st.text_input("Nombre", value=sel if modo == "Editar uno existente" else "")
            cat = st.text_input("Categoría", value=actual["categoria"])
            unidad = st.text_input("Unidad (Pieza, cm2, Metro, ML, Gramo...)", value=actual["unidad"])
            costo = st.number_input("Costo por unidad", min_value=0.0, value=float(actual["costo"]), step=0.5)
            nota = st.text_input("Nota (opcional)", value=actual["nota"])
            if st.form_submit_button("💾 Guardar material"):
                if nombre.strip():
                    datos["materiales"][nombre] = {"categoria": cat or "GENERAL", "unidad": unidad,
                                                    "costo": costo, "nota": nota}
                    guardar_estado()
                    st.success(f"'{nombre}' guardado. Los productos que lo usan ya quedaron actualizados.")
                    st.rerun()
                else:
                    st.error("El nombre no puede estar vacío.")

    with st.expander("🗑️ Eliminar material"):
        if existentes:
            n = st.selectbox("Material a eliminar", existentes, key="del_mat")
            if st.button("Eliminar definitivamente"):
                usados = [p for p, v in datos["productos"].items()
                          if any(i["material"] == n for i in v["materiales"])]
                if usados:
                    st.error(f"Lo usan: {', '.join(usados)}. Quítalo de esos productos primero.")
                else:
                    del datos["materiales"][n]
                    guardar_estado()
                    st.success("Eliminado.")
                    st.rerun()

    with st.expander("📐 Calculadora de costo por área (vinil, acrílico, papel, MDF)"):
        precio_l = st.number_input("Precio del lienzo/pliego COMPLETO", min_value=0.0, step=1.0)
        largo = st.number_input("Largo (cm)", min_value=0.0, step=1.0)
        ancho = st.number_input("Ancho (cm)", min_value=0.0, step=1.0)
        if largo and ancho:
            area = largo * ancho
            costo_cm2 = precio_l / area if area else 0
            st.info(f"Área total: {area:g} cm² → Costo por cm²: **${costo_cm2:,.4f}**")
            nombre_m = st.text_input("Nombre para guardar este material", key="area_nombre")
            cat_m = st.text_input("Categoría", key="area_cat")
            if st.button("Guardar como material por cm²"):
                if nombre_m:
                    datos["materiales"][nombre_m] = {
                        "categoria": cat_m or "GENERAL", "unidad": "cm2", "costo": costo_cm2,
                        "nota": f"Lienzo {largo:g}x{ancho:g} a ${precio_l:,.2f}"}
                    guardar_estado()
                    st.success("Guardado. Ya puedes usarlo por cm² en tus recetas.")
                    st.rerun()


# =========================================================
#  PÁGINA: MANO DE OBRA Y MÁQUINAS
# =========================================================
elif pagina == "🛠️ Mano de obra y Máquinas":
    st.title("🛠️ Mano de obra y Máquinas")
    tab1, tab2 = st.tabs(["👩‍🎨 Actividades", "🖨️ Máquinas"])

    with tab1:
        df = pd.DataFrame([{"Actividad": k, "Precio/hora": v, "Precio/min": v / 60}
                            for k, v in datos["actividades"].items()]).sort_values("Actividad")
        st.dataframe(df.style.format({"Precio/hora": "${:,.2f}", "Precio/min": "${:,.3f}"}),
                     use_container_width=True, hide_index=True)
        with st.expander("➕ Agregar / editar actividad"):
            with st.form("form_act"):
                nombre = st.text_input("Nombre de la actividad")
                precio = st.number_input("Precio por hora", min_value=0.0, step=5.0)
                if st.form_submit_button("💾 Guardar"):
                    if nombre.strip():
                        datos["actividades"][nombre] = precio
                        guardar_estado(); st.success("Guardado."); st.rerun()
        with st.expander("🗑️ Eliminar actividad"):
            n = st.selectbox("Actividad", sorted(datos["actividades"]), key="del_act")
            if st.button("Eliminar", key="btn_del_act"):
                usados = [p for p, v in datos["productos"].items()
                          if any(i["actividad"] == n for i in v["actividades"])]
                if usados:
                    st.error(f"La usan: {', '.join(usados)}")
                else:
                    del datos["actividades"][n]; guardar_estado(); st.success("Eliminada."); st.rerun()

    with tab2:
        df = pd.DataFrame([{"Máquina": k, "Desgaste/hora": v, "Desgaste/min": v / 60}
                            for k, v in datos["maquinas"].items()]).sort_values("Máquina")
        st.dataframe(df.style.format({"Desgaste/hora": "${:,.2f}", "Desgaste/min": "${:,.3f}"}),
                     use_container_width=True, hide_index=True)
        with st.expander("➕ Agregar / editar máquina"):
            with st.form("form_maq"):
                nombre = st.text_input("Nombre de la máquina")
                costo = st.number_input("Costo de desgaste por hora", min_value=0.0, step=1.0)
                if st.form_submit_button("💾 Guardar"):
                    if nombre.strip():
                        datos["maquinas"][nombre] = costo
                        guardar_estado(); st.success("Guardado."); st.rerun()
        with st.expander("🗑️ Eliminar máquina"):
            n = st.selectbox("Máquina", sorted(datos["maquinas"]), key="del_maq")
            if st.button("Eliminar", key="btn_del_maq"):
                usados = [p for p, v in datos["productos"].items()
                          if any(i["maquina"] == n for i in v["maquinas"])]
                if usados:
                    st.error(f"La usan: {', '.join(usados)}")
                else:
                    del datos["maquinas"][n]; guardar_estado(); st.success("Eliminada."); st.rerun()


# =========================================================
#  PÁGINA: GASTOS FIJOS
# =========================================================
elif pagina == "🏢 Gastos fijos":
    st.title("🏢 Gastos fijos mensuales")
    g = datos["gastos_fijos"]

    with st.form("form_gastos"):
        c1, c2, c3 = st.columns(3)
        with c1:
            g["renta"] = st.number_input("Renta", value=float(g["renta"]), step=50.0)
            g["luz"] = st.number_input("Luz", value=float(g["luz"]), step=10.0)
            g["agua"] = st.number_input("Agua", value=float(g["agua"]), step=10.0)
        with c2:
            g["internet"] = st.number_input("Internet", value=float(g["internet"]), step=10.0)
            g["apps"] = st.number_input("Apps", value=float(g["apps"]), step=10.0)
            g["adobe"] = st.number_input("Adobe", value=float(g["adobe"]), step=10.0)
        with c3:
            g["gasolina"] = st.number_input("Gasolina", value=float(g["gasolina"]), step=50.0)
            g["mantenimiento"] = st.number_input("Mantenimiento", value=float(g["mantenimiento"]), step=10.0)
            g["dominio"] = st.number_input("Dominio", value=float(g["dominio"]), step=10.0)

        c4, c5 = st.columns(2)
        with c4: g["dias_mes"] = st.number_input("Días de trabajo al mes", value=float(g["dias_mes"]), step=1.0)
        with c5: g["horas_dia"] = st.number_input("Horas de trabajo al día", value=float(g["horas_dia"]), step=0.5)

        if st.form_submit_button("💾 Guardar gastos fijos"):
            guardar_estado(); st.success("Actualizado.")

    total, horas, c_hora, c_min = calcular_gastos_fijos(datos)
    c1, c2, c3 = st.columns(3)
    with c1: card(f"<div class='ohana-badge'>TOTAL MENSUAL</div><h2>${total:,.2f}</h2>")
    with c2: card(f"<div class='ohana-badge'>COSTO/HORA</div><h2>${c_hora:,.2f}</h2>{horas:g} horas al mes")
    with c3: card(f"<div class='ohana-badge'>COSTO/MINUTO</div><h2>${c_min:,.3f}</h2>se usa en cada producto")


# =========================================================
#  PÁGINA: PRODUCTOS Y SERVICIOS
# =========================================================
elif pagina == "📦 Productos y Servicios":
    st.title("📦 Productos y Servicios")

    opciones_p = ["➕ Nuevo producto/servicio"] + sorted(datos["productos"].keys())
    seleccion = st.selectbox("Selecciona o crea uno nuevo", opciones_p)

    base_vacio = {"tipo": "producto", "materiales": [], "actividades": [], "maquinas": [],
                  "minutos_proceso": 0.0, "otros_costos": 0.0, "unidades_lote": 1.0,
                  "margen_pct": None, "descripcion": "", "categoria": "", "foto": "", "publicado": False}

    if seleccion == "➕ Nuevo producto/servicio":
        if st.session_state.get("draft_de") != "__nuevo__":
            st.session_state["draft"] = copy.deepcopy(base_vacio)
            st.session_state["draft_de"] = "__nuevo__"
            st.session_state["draft_nombre"] = ""
    else:
        if st.session_state.get("draft_de") != seleccion:
            st.session_state["draft"] = copy.deepcopy(datos["productos"][seleccion])
            st.session_state["draft_de"] = seleccion
            st.session_state["draft_nombre"] = seleccion

    draft = st.session_state["draft"]

    col1, col2, col3 = st.columns([2, 1, 1])
    nombre = col1.text_input("Nombre del producto/servicio", value=st.session_state["draft_nombre"])
    draft["tipo"] = col2.radio("Tipo", ["producto", "servicio"],
                                index=0 if draft["tipo"] == "producto" else 1, horizontal=True)
    draft["unidades_lote"] = col3.number_input("Piezas por lote", min_value=1.0,
                                                value=float(draft["unidades_lote"]))

    st.markdown("---")

    if draft["tipo"] == "producto":
        st.subheader("🧵 Materiales usados")
        categorias = sorted(set(m["categoria"] for m in datos["materiales"].values()))
        if categorias:
            c1, c2, c3, c4 = st.columns([1.2, 1.5, 0.8, 0.6])
            cat_sel = c1.selectbox("Categoría", categorias, key="pcat")
            nombres_cat = sorted(n for n, m in datos["materiales"].items() if m["categoria"] == cat_sel)
            mat_sel = c2.selectbox("Material", nombres_cat, key="pmat")
            cant = c3.number_input("Cantidad (lote)", min_value=0.0, step=1.0, key="pcant")
            c4.write("")
            if c4.button("Agregar", key="btn_pm"):
                existe = next((i for i in draft["materiales"] if i["material"] == mat_sel), None)
                if existe: existe["cantidad"] = cant
                else: draft["materiales"].append({"material": mat_sel, "cantidad": cant})
                st.rerun()

        for i, it in enumerate(draft["materiales"]):
            m = datos["materiales"].get(it["material"], {"unidad": "?", "costo": 0})
            sub = it["cantidad"] * m["costo"]
            cc1, cc2 = st.columns([5, 1])
            cc1.write(f"• **{it['material']}** — {it['cantidad']:g} {m['unidad']} → ${sub:,.2f}")
            if cc2.button("🗑️", key=f"delm{i}"):
                draft["materiales"].pop(i); st.rerun()

    st.subheader("👩‍🎨 Mano de obra")
    if datos["actividades"]:
        c1, c2, c3 = st.columns([2, 1, 0.6])
        act_sel = c1.selectbox("Actividad", sorted(datos["actividades"]), key="pact")
        mins = c2.number_input("Minutos (lote)", min_value=0.0, step=1.0, key="pactmin")
        c3.write("")
        if c3.button("Agregar", key="btn_pa"):
            existe = next((i for i in draft["actividades"] if i["actividad"] == act_sel), None)
            if existe: existe["minutos"] = mins
            else: draft["actividades"].append({"actividad": act_sel, "minutos": mins})
            st.rerun()

    for i, it in enumerate(draft["actividades"]):
        ph = datos["actividades"].get(it["actividad"], 0)
        sub = it["minutos"] * (ph / 60)
        cc1, cc2 = st.columns([5, 1])
        cc1.write(f"• **{it['actividad']}** — {it['minutos']:g} min → ${sub:,.2f}")
        if cc2.button("🗑️", key=f"dela{i}"):
            draft["actividades"].pop(i); st.rerun()

    st.subheader("🖨️ Máquinas usadas")
    if datos["maquinas"]:
        c1, c2, c3 = st.columns([2, 1, 0.6])
        maq_sel = c1.selectbox("Máquina", sorted(datos["maquinas"]), key="pmaq")
        minsm = c2.number_input("Minutos (lote)", min_value=0.0, step=1.0, key="pmaqmin")
        c3.write("")
        if c3.button("Agregar", key="btn_pq"):
            existe = next((i for i in draft["maquinas"] if i["maquina"] == maq_sel), None)
            if existe: existe["minutos"] = minsm
            else: draft["maquinas"].append({"maquina": maq_sel, "minutos": minsm})
            st.rerun()

    for i, it in enumerate(draft["maquinas"]):
        ch = datos["maquinas"].get(it["maquina"], 0)
        sub = it["minutos"] * (ch / 60)
        cc1, cc2 = st.columns([5, 1])
        cc1.write(f"• **{it['maquina']}** — {it['minutos']:g} min → ${sub:,.2f}")
        if cc2.button("🗑️", key=f"delq{i}"):
            draft["maquinas"].pop(i); st.rerun()

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    draft["minutos_proceso"] = c1.number_input("Minutos totales del proceso (gastos fijos)",
                                                min_value=0.0, value=float(draft["minutos_proceso"]), step=1.0)
    draft["otros_costos"] = c2.number_input("Otros costos del lote", min_value=0.0,
                                             value=float(draft["otros_costos"]), step=1.0)
    margen_actual = draft.get("margen_pct")
    usar_propio = c3.checkbox("Margen propio", value=margen_actual is not None)
    if usar_propio:
        draft["margen_pct"] = c3.number_input("Margen %", min_value=0.0, max_value=95.0,
                                               value=float(margen_actual or datos["config"]["margen_pct"]))
    else:
        draft["margen_pct"] = None

    st.markdown("---")
    st.subheader("🛍️ Datos para el catálogo público")
    c1, c2 = st.columns(2)
    draft["categoria"] = c1.text_input("Categoría de catálogo (ej. Playeras, Cajas, Llaveros)",
                                        value=draft.get("categoria", ""))
    draft["publicado"] = c2.checkbox("✅ Mostrar en el catálogo público",
                                      value=draft.get("publicado", False))
    draft["descripcion"] = st.text_area("Descripción corta para clientas",
                                         value=draft.get("descripcion", ""))

    foto_actual = draft.get("foto", "")
    if foto_actual and os.path.exists(foto_actual):
        st.image(foto_actual, width=180, caption="Foto actual")
    subida = st.file_uploader("Subir foto del producto", type=["png", "jpg", "jpeg"])
    if subida is not None:
        ruta = os.path.join(CARPETA_FOTOS, subida.name).replace("\\", "/")
        with open(ruta, "wb") as f:
            f.write(subida.getbuffer())
        draft["foto"] = ruta
        st.success(f"Foto guardada: {ruta}")

    col_g, col_d = st.columns(2)
    if col_g.button("💾 Guardar producto"):
        if not nombre.strip():
            st.error("Ponle un nombre al producto.")
        else:
            if seleccion != "➕ Nuevo producto/servicio" and seleccion != nombre:
                del datos["productos"][seleccion]
            datos["productos"][nombre] = draft
            guardar_estado()
            st.session_state["draft_de"] = nombre
            st.session_state["draft_nombre"] = nombre
            st.success(f"'{nombre}' guardado correctamente.")
            st.rerun()

    if seleccion != "➕ Nuevo producto/servicio":
        if col_d.button("🗑️ Eliminar este producto"):
            del datos["productos"][seleccion]
            guardar_estado()
            st.session_state["draft_de"] = None
            st.success("Eliminado.")
            st.rerun()

    if nombre.strip():
        st.markdown("## 📊 Resultado")
        r = calcular(datos, draft)
        colA, colB = st.columns([1.3, 1])
        with colA:
            card(f"""
            <b>Materiales:</b> ${r['costo_materiales']:,.2f}<br>
            <b>Mano de obra:</b> ${r['costo_mano_obra']:,.2f}<br>
            <b>Máquinas:</b> ${r['costo_maquinas']:,.2f}<br>
            <b>Gastos fijos:</b> ${r['indirectos']:,.2f}<br>
            <b>Otros:</b> ${r['otros']:,.2f}<br><hr>
            <b>Costo total del lote:</b> ${r['costo_total']:,.2f}<br>
            <b>Costo por unidad:</b> ${r['costo_unit']:,.2f}
            """)
        with colB:
            st.markdown(f"""
            <div class="price-box">
                <div class="label">PRECIO FINAL SUGERIDO</div>
                <div class="value">${r['precio_final']:,.2f}</div>
                <div class="label">Ganancia: ${r['ganancia']:,.2f} · Margen {r['margen']:g}%</div>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
#  PÁGINA: LISTA DE PRECIOS
# =========================================================
elif pagina == "💲 Lista de precios":
    st.title("💲 Lista de precios (interna)")
    if not datos["productos"]:
        st.info("Aún no has creado productos.")
    else:
        filas = []
        for n, p in datos["productos"].items():
            r = calcular(datos, p)
            filas.append({"Producto": n, "Tipo": p["tipo"], "En catálogo": "Sí" if p.get("publicado") else "No",
                          "Costo unitario": r["costo_unit"], "Precio final": r["precio_final"],
                          "Ganancia": r["ganancia"]})
        df = pd.DataFrame(filas).sort_values("Producto")
        st.dataframe(df.style.format({"Costo unitario": "${:,.2f}", "Precio final": "${:,.2f}",
                                       "Ganancia": "${:,.2f}"}),
                     use_container_width=True, hide_index=True, height=450)
        st.download_button("⬇️ Descargar como CSV", df.to_csv(index=False).encode("utf-8"),
                            "lista_precios_ohana.csv", "text/csv")


# =========================================================
#  PÁGINA: CONFIGURACIÓN
# =========================================================
elif pagina == "⚙️ Configuración":
    st.title("⚙️ Configuración general")
    c = datos["config"]
    with st.form("form_config"):
        c["moneda"] = st.text_input("Símbolo de moneda", value=c["moneda"])
        c["margen_pct"] = st.number_input("Margen de ganancia general (%)", min_value=0.0, max_value=95.0,
                                           value=float(c["margen_pct"]))
        c["impuesto_pct"] = st.number_input("Impuesto (%)", min_value=0.0, value=float(c["impuesto_pct"]))
        c["redondeo"] = st.number_input("Redondear precio final hacia arriba a múltiplos de",
                                         min_value=0.0, value=float(c["redondeo"]), step=0.5)
        if st.form_submit_button("💾 Guardar configuración"):
            guardar_estado()
            st.success("Configuración guardada.")
