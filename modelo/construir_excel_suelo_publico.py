"""Genera modelo/memoria-suelo-publico.xlsx con fórmulas vivas que replican modelo_suelo_publico.py
(régimen B, paridad del IGV). Ejecutar: python3 modelo/construir_excel_suelo_publico.py y luego recalcular."""
import json
import os

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Font, PatternFill

import modelo_multifamily as m1
import modelo_suelo_publico as sp

HERE = os.path.dirname(os.path.abspath(__file__))
RES = json.load(open(os.path.join(HERE, "resultados_suelo_publico.json")))
B, SP = m1.BASE, sp.SP

F = "Arial"
BLUE = Font(name=F, color="0000FF"); BLACK = Font(name=F); GREEN = Font(name=F, color="008000")
BOLD = Font(name=F, bold=True); TITLE = Font(name=F, bold=True, size=13)
HDR = PatternFill("solid", fgColor="DDEBF7"); YEL = PatternFill("solid", fgColor="FFFF00")
NUM = '#,##0;(#,##0);"-"'; NUM1 = '#,##0.0;(#,##0.0);"-"'; PCT = '0.0%;(0.0%);"-"'; PCT2 = '0.00%;(0.00%);"-"'
TMAX = 90  # filas t = 0..90 (T1 + T2 hasta 90)

wb = Workbook()

# ------------------------------------------------------------------ Léeme
ws = wb.active; ws.title = "Leeme"
lines = [
    ("Memoria de cálculo: vivienda en renta sobre suelo público en derecho de superficie (Lima-Callao)", TITLE),
    ("Réplica en fórmulas del script modelo/modelo_suelo_publico.py. Caso base = régimen B (paridad del IGV).", None),
    ("", None),
    ("Cómo usar", BOLD),
    ("1. Los supuestos editables están en la hoja Supuestos en azul; los clave, con fondo amarillo.", None),
    ("2. Flujos calcula año por año (t = 0 es la entrega del terreno) la cascada inversionistas → Estado → excedente.", None),
    ("3. Resumen muestra los resultados y los compara con Python (control).", None),
    ("4. Escenarios, Sensibilidad y Plazos son tablas de valores generadas por el script (no se recalculan aquí).", None),
    ("5. Asequibilidad calcula con fórmulas el bono a la familia y la brecha de pago por nivel de ingreso.", None),
    ("", None),
    ("Convenciones", BOLD),
    ("Soles nominales por m2 vendible (multiplicar por 5,500 m2 para un edificio de ~100 departamentos). Antes de IR.", None),
    ("Azul = dato ingresado · Negro = fórmula · Verde = vínculo a otra hoja.", None),
    ("Límites: T1 + T2 ≤ 90 años; esta hoja solo modela el régimen B (el A, IGV actual, está en el script: escenario E0).", None),
    ("Cascada: el flujo del proyecto paga primero a los inversionistas hasta su retorno r_inv; luego al Estado hasta", None),
    ("recuperar el terreno con r_est; el excedente se reparte. En T1 el edificio revierte al Estado sin pago y este cobra", None),
    ("al nuevo operador el valor de un segundo periodo de T2 años (relicitación). No hay conversión a venta.", None),
]
for i, (t, f) in enumerate(lines, 1):
    ws.cell(i, 1, t).font = f or BLACK
ws.column_dimensions["A"].width = 120

# ------------------------------------------------------------------ Supuestos
S = wb.create_sheet("Supuestos")
S["A1"] = "Supuestos (valores base al 26-nov-2026)"; S["A1"].font = TITLE
for j, h in enumerate(["Parámetro", "Valor", "Unidad", "Fuente / sustento"], 1):
    c = S.cell(3, j + 1, h); c.font = BOLD; c.fill = HDR
ren = dict(SP["renov"])
rows = [
    ("sec", "Mercado y operación (iguales al artículo 1)"),
    ("tc", "Tipo de cambio", B["tc"], "S/ por US$", "BCRP, interbancario nov-2026", "0.00", False),
    ("renta_usd", "Alquiler de oferta Lima Moderna", B["renta_oferta_usd"], "US$/m2/año", "BCRP, Nota de Estudios 16-2026 (promedio de 6 distritos)", "0.0", True),
    ("desc", "Descuento oferta a cierre", B["desc_cierre"], "%", "Estimación (igual que artículo 1)", PCT, False),
    ("gr", "Crecimiento nominal de la renta", B["g_renta"], "% anual", "Inflación de largo plazo ~2.5%; sin crecimiento real", PCT, False),
    ("gc", "Crecimiento del costo de construcción", B["g_costo"], "% anual", "Estimación (índices INEI)", PCT, False),
    ("go", "Crecimiento del opex", B["g_opex"], "% anual", "Estimación", PCT, False),
    ("incob", "Incobrables", B["incobrable"], "% de la renta", "Estimación", PCT, False),
    ("oe", "Ocupación estabilizada", B["ocup_estab"], "%", "Estimación de mercado; verificar con operadores", PCT, False),
    ("opex", "Opex sin IGV", B["opex_m2"], "S/ por m2/año", "Desglose en memoria del artículo 1", NUM1, False),
    ("fijo", "Parte fija del opex", B["opex_fijo"], "%", "Estimación", PCT, False),
    ("grav", "Parte del opex gravada con IGV", B["opex_gravado"], "%", "Estimación", PCT, False),
    ("igv", "IGV", B["igv"], "%", "TUO Ley del IGV (16% + 2% IPM)", PCT, False),
    ("res", "Reserva de capex", B["reserva_capex"], "% de la renta", "Estimación", PCT, False),
    ("sec", "Costo de desarrollo (sin terreno, t0)"),
    ("cd", "Costo directo", B["cd_m2"], "S/ por m2 vendible", "CAPECO / presupuestos; ver memoria art. 1", NUM, False),
    ("indp", "Indirectos", B["ind_pct"], "% del directo", "Estimación", PCT, False),
    ("contp", "Contingencia", B["cont_pct"], "% del directo", "Estimación", PCT, False),
    ("indg", "Parte gravada de los indirectos", B["ind_gravado"], "%", "Estimación", PCT, False),
    ("ffe", "Mobiliario y equipamiento (FF&E)", B["ffe_m2"], "S/ por m2", "Estimación", NUM, False),
    ("mkt", "Comercialización BTR", B["mkt_btr_m2"], "S/ por m2", "Estimación", NUM, False),
    ("fcosto", "Factor de costo (sensibilidad)", SP["f_costo"], "x", "1.00 = base", "0.00", False),
    ("sec", "Ubicación y producto"),
    ("frenta", "Factor de alquiler de la ubicación", SP["f_renta"], "x", "1.00 = Lima Moderna; 0.80 ≈ periferia", "0.00", True),
    ("drenta", "Descuento al inquilino financiado por el proyecto", SP["desc_renta"], "%", "0% en la propuesta: la asequibilidad va por bono visible", PCT, False),
    ("L", "Valor de mercado del terreno", RES["supuestos"]["L"], "S/ por m2 vendible", "Residual BTS del artículo 1 (TIR 20%); vínculo manual al modelo 1", NUM1, True),
    ("sec", "Estructura de la concesión"),
    ("rinv", "Costo combinado del capital por etapas", SP["r_inv"], "% anual", "Supuesto clave: mezcla mini-perm + bonos/FIBRA/AFP en soles; ver memoria §3", PCT, True),
    ("rest", "Costo de financiamiento del Estado", SP["r_est"], "% anual", "Bono soberano 10 años en soles ~6.3% (BCRP/MEF, nov-2026; verificar)", PCT, True),
    ("T1", "Primer periodo del derecho de superficie", SP["T1"], "años", "Propuesta; Código Civil art. 1030: máximo 99 años", "0", True),
    ("T2", "Segundo periodo (relicitación)", SP["T2"], "años", "Propuesta", "0", False),
    ("split", "Excedente que va al Estado", SP["split"], "%", "Propuesta; se compite en la licitación", PCT, False),
    ("s1", "Desembolso de obra año 1", SP["sched"][0], "%", "Calendario de 3 años", PCT, False),
    ("s2", "Desembolso de obra año 2", SP["sched"][1], "%", "", PCT, False),
    ("s3", "Desembolso de obra año 3", SP["sched"][2], "%", "", PCT, False),
    ("o3", "Ocupación año 3", SP["ocup"][0], "%", "Obra en curso", PCT, False),
    ("o4", "Ocupación año 4", SP["ocup"][1], "%", "Colocación", PCT, False),
    ("r1a", "Renovación mayor 1: año", 20, "año", "Estimación", "0", False),
    ("r1p", "Renovación mayor 1: % del costo", ren[20], "%", "", PCT, False),
    ("r2a", "Renovación mayor 2: año", 35, "año", "No se ejecuta si cae en los 2 últimos años de T1", "0", False),
    ("r2p", "Renovación mayor 2: % del costo", ren[35], "%", "", PCT, False),
    ("rrel", "Renovación que asume el nuevo operador", SP["renov_relic"], "% del costo", "Se descuenta del valor de relicitación", PCT, False),
    ("frel", "Factor sobre el valor de relicitación", SP["f_relic"], "x", "1.00 = base", "0.00", False),
    ("rlp", "Retorno del inversionista de largo plazo", SP["r_lp"], "% anual", "Comprador del activo estabilizado (FIBRA/AFP)", PCT, False),
    ("tv", "Año de venta a largo plazo", SP["t_venta"], "año", "", "0", False),
    ("sec", "Derivados (fórmulas)"),
    ("costo", "Costo de desarrollo sin IGV", "=({cd}+{cd}*{indp}+{cd}*{contp}+{ffe}+{mkt})*{fcosto}", "S/ por m2", "", NUM1, False),
    ("igvo", "IGV de obra (costo en régimen B)", "=({cd}+{cd}*{contp}+{cd}*{indp}*{indg}+{ffe}+{mkt})*{igv}*{fcosto}", "S/ por m2", "", NUM1, False),
    ("capex", "Capex total régimen B", "={costo}+{igvo}", "S/ por m2", "", NUM1, False),
    ("renta0", "Alquiler de cierre t0", "={renta_usd}*{tc}*(1-{desc})*{frenta}*(1-{drenta})", "S/ por m2 alquilado/año", "", NUM1, False),
]
N = {}
r = 4
for row in rows:
    if row[0] == "sec":
        S.cell(r, 2, row[1]).font = BOLD; r += 1; continue
    N[row[0]] = f"Supuestos!$C${r}"
    r += 1
r = 4
for row in rows:
    if row[0] == "sec":
        r += 1; continue
    k, lab, val, unit, src, fmt, key = row
    S.cell(r, 2, lab).font = BLACK
    loc = {kk: v.replace("Supuestos!", "") for kk, v in N.items()}
    c = S.cell(r, 3, val.format(**loc) if isinstance(val, str) else val)
    c.font = BLACK if isinstance(val, str) else BLUE
    c.number_format = fmt
    if key:
        c.fill = YEL
    S.cell(r, 4, unit).font = BLACK
    S.cell(r, 5, src).font = BLACK
    r += 1
S.column_dimensions["B"].width = 46; S.column_dimensions["C"].width = 14
S.column_dimensions["D"].width = 22; S.column_dimensions["E"].width = 80

# ------------------------------------------------------------------ Flujos
W = wb.create_sheet("Flujos")
W["A1"] = "Flujos anuales y cascada (S/ por m2 vendible, nominales)"; W["A1"].font = TITLE
cols = ["t", "Esc. costo", "Ocupación", "Obra", "Renta", "Opex+IGV", "Reserva", "NOI", "Renovación",
        "Flujo proyecto", "VP NOI relicit.", "Saldo inv. previo", "Saldo Estado previo", "A inversionistas",
        "A Estado", "Excedente", "Saldo inv.", "Saldo Estado", "Flujo inversionistas", "Flujo Estado",
        "VP a largo plazo", "Flujo desarrollo", "Año recupera"]
for j, h in enumerate(cols, 1):
    c = W.cell(4, j, h); c.font = BOLD; c.fill = HDR
R0 = 5
n = lambda k: N[k]
for t in range(TMAX + 1):
    i = R0 + t
    p = i - 1
    f = {}
    f["A"] = t
    f["B"] = f"=(1+{n('gc')})^A{i}"
    f["C"] = f"=IF(A{i}=3,{n('o3')},IF(A{i}=4,{n('o4')},IF(A{i}>=5,{n('oe')},0)))"
    f["D"] = f"=-{n('capex')}*IF(A{i}=1,{n('s1')},IF(A{i}=2,{n('s2')},IF(A{i}=3,{n('s3')},0)))*B{i}"
    f["E"] = f"={n('renta0')}*(1+{n('gr')})^A{i}*C{i}*(1-{n('incob')})"
    f["F"] = (f"=IF(C{i}>0,-{n('opex')}*(1+{n('go')})^A{i}*({n('fijo')}+(1-{n('fijo')})*C{i}/{n('oe')})"
              f"*(1+{n('grav')}*{n('igv')}),0)")
    f["G"] = f"=-{n('res')}*E{i}"
    f["H"] = f"=E{i}+F{i}+G{i}"
    f["I"] = (f"=-IF(A{i}>{n('T1')}-3,0,IF(A{i}={n('r1a')},{n('r1p')},IF(A{i}={n('r2a')},{n('r2p')},0)))"
              f"*{n('costo')}*B{i}")
    f["J"] = f"=IF(A{i}<={n('T1')},D{i}+H{i}+I{i},0)"
    f["K"] = f"=IF(AND(A{i}>{n('T1')},A{i}<={n('T1')}+{n('T2')}),H{i}/(1+{n('rinv')})^(A{i}-{n('T1')}),0)"
    f["L"] = "=0" if t == 0 else f"=Q{p}*(1+{n('rinv')})"
    f["M"] = f"={n('L')}" if t == 0 else f"=R{p}*(1+{n('rest')})"
    f["N"] = f"=IF(J{i}<0,J{i},MIN(J{i},L{i}))"
    f["O"] = f"=IF(J{i}<0,0,MIN(J{i}-N{i},M{i}))"
    f["P"] = f"=IF(J{i}<0,0,J{i}-N{i}-O{i})"
    f["Q"] = f"=IF(J{i}<0,L{i}-J{i},L{i}-N{i})"
    f["R"] = f"=M{i}-O{i}"
    f["S"] = f"=IF(J{i}<0,J{i},N{i}+P{i}*(1-{n('split')}))"
    f["T"] = (f"=IF(A{i}=0,-{n('L')},0)+O{i}+P{i}*{n('split')}+IF(A{i}={n('T1')},Resumen!$C$6,0)")
    f["U"] = f"=IF(AND(A{i}>{n('tv')},A{i}<={n('T1')}),S{i}/(1+{n('rlp')})^(A{i}-{n('tv')}),0)"
    f["V"] = f"=IF(A{i}<{n('tv')},S{i},IF(A{i}={n('tv')},S{i}+Resumen!$C$15,0))"
    f["W"] = f"=IF(AND(A{i}>0,A{i}<={n('T1')},R{i}<=0.000001),A{i},999)"
    for col, val in f.items():
        c = W[f"{col}{i}"]; c.value = val
        c.font = BLUE if col == "A" else BLACK
        c.number_format = "0" if col in ("A", "W") else (PCT if col == "C" else ("0.000" if col == "B" else NUM1))
W.freeze_panes = "B5"
for j in range(2, 24):
    W.column_dimensions[chr(64 + j)].width = 13
RL = R0 + TMAX
rng = lambda col, a=R0: f"Flujos!{col}{a}:{col}{RL}"

# ------------------------------------------------------------------ Resumen
Rz = wb.create_sheet("Resumen", 1)
Rz["A1"] = "Resumen del caso base (E4, propuesta) y control contra Python"; Rz["A1"].font = TITLE
for j, h in enumerate(["Indicador", "Excel", "Python", "Diferencia", "Nota"], 2):
    c = Rz.cell(4, j, h); c.font = BOLD; c.fill = HDR
b = RES["base"]
idx = lambda col: f"INDEX({rng(col)},{n('T1')}+1)"
res_rows = [
    ("Terreno a valor de mercado (S/ por m2)", f"={n('L')}", b["L"], NUM1, "Aporte del Estado, subordinado"),
    ("Valor de relicitación cobrado en T1", f"=(SUM({rng('K')})-{n('rrel')}*{n('costo')}*(1+{n('gc')})^{n('T1')})*{n('frel')}",
     b["fee"], NUM1, "VP a r_inv del NOI de T2, menos renovación del nuevo operador"),
    ("TIR del proyecto (sin terreno)", f"=IRR({rng('J')},0.08)", b["tir_proy"], PCT2, "Flujo hasta T1"),
    ("TIR de los inversionistas", f"=IRR({rng('S')},0.08)", b["tir_inv"], PCT2, "Meta = r_inv"),
    ("¿Inversionistas recuperan su retorno?", f'=IF({idx("Q")}<=0.000001,"Sí","No")', "Sí" if b["inv_ok"] else "No", None, "Saldo al cierre de T1 = 0"),
    ("TIR del Estado sobre su terreno", f"=IRR({rng('T')},0.06)", b["tir_est"], PCT2, "Meta ≥ r_est"),
    ("VPN del Estado a r_est", f"=Flujos!T{R0}+NPV({n('rest')},Flujos!T{R0+1}:T{RL})", b["vpn_est_rest"], NUM1, "≥ 0 = no hay subsidio en valor presente"),
    ("VPN del Estado a 9%", f"=Flujos!T{R0}+NPV(0.09,Flujos!T{R0+1}:T{RL})", b["vpn_est_9"], NUM1, "Costo de oportunidad privado (referencia)"),
    ("Año en que el Estado recupera el terreno",
     f'=IF(MIN({rng("W")})<999,MIN({rng("W")}),IF(C6>={idx("R")}-C6*0+0,{n("T1")},"No recupera"))',
     b["rec"] if b["rec"] is not None else "No recupera", "0", "Incluye el cobro de la relicitación"),
    ("Yield on cost año 6 (sin terreno)", f"=Flujos!H{R0+6}/({n('capex')}*({n('s1')}+{n('s2')}+{n('s3')}))", b["yoc"], PCT2, "NOI / capex a precios t0"),
    ("Precio de venta al inversionista de largo plazo", f"=SUM({rng('U')})", b["precio_lp"], NUM1, "En el año tv, a r_lp"),
    ("TIR de la etapa de desarrollo", f"=IRR(Flujos!V{R0}:V{R0+SP['t_venta']},0.1)", b["tir_dev"], PCT2, "Desarrollo + venta del activo estabilizado"),
]
# Fila del valor de relicitación = 6, precio LP = 15 (referenciadas desde Flujos)
for k, (lab, xl, py, fmt, note) in enumerate(res_rows):
    i = 5 + k
    Rz.cell(i, 2, lab).font = BLACK
    c = Rz.cell(i, 3, xl); c.font = BLACK
    if fmt: c.number_format = fmt
    c2 = Rz.cell(i, 4, py); c2.font = BLUE
    if fmt: c2.number_format = fmt
    if isinstance(py, (int, float)) and fmt:
        d = Rz.cell(i, 5, f"=C{i}-D{i}"); d.number_format = fmt; d.font = BLACK
    Rz.cell(i, 6, note).font = BLACK
# corregir referencia del año de recuperación: comparar relicitación (C6) con saldo previo al cobro en T1
Rz["C13"] = f'=IF(MIN({rng("W")})<999,MIN({rng("W")}),IF(C6>={idx("R")},{n("T1")},"No recupera"))'
Rz["C13"].number_format = "0"
assert Rz["B6"].value.startswith("Valor de relicitación") and Rz["B15"].value.startswith("Precio de venta")
Rz["B19"] = "Lectura"; Rz["B19"].font = BOLD
Rz["B20"] = ("El Estado no subsidia si el VPN a r_est es ≥ 0. Con el caso base el margen es pequeño: ver Sensibilidad "
             "(alquiler −10% o costo +10% lo vuelven negativo).")
Rz["B21"] = "Las columnas Python son valores pegados del script como control; la diferencia debe ser ~0."
Rz.column_dimensions["B"].width = 48; Rz.column_dimensions["C"].width = 14; Rz.column_dimensions["D"].width = 14
Rz.column_dimensions["E"].width = 12; Rz.column_dimensions["F"].width = 60

# ------------------------------------------------------------------ Escenarios / Sensibilidad / Plazos (valores)
def tabla(nombre, titulo, hdr, data):
    sh = wb.create_sheet(nombre)
    sh["A1"] = titulo; sh["A1"].font = TITLE
    sh["A2"] = "Valores generados por modelo/modelo_suelo_publico.py (no se recalculan en esta hoja)."
    for j, h in enumerate(hdr, 1):
        c = sh.cell(4, j, h[0]); c.font = BOLD; c.fill = HDR
        sh.column_dimensions[chr(64 + j)].width = h[2]
    for i, row in enumerate(data, 5):
        for j, h in enumerate(hdr, 1):
            v = row.get(h[1])
            if isinstance(v, bool):
                v = "Sí" if v else "No"
            if v is None:
                v = "—"
            c = sh.cell(i, j, v); c.font = BLUE
            if h[3]: c.number_format = h[3]
    return sh

tabla("Escenarios", "Escenarios (S/ por m2 vendible)", [
    ("Id", "id", 6, None), ("Escenario", "nombre", 62, None), ("TIR proyecto", "tir_proy", 13, PCT2),
    ("TIR inversionistas", "tir_inv", 15, PCT2), ("¿Cumple r_inv?", "inv_ok", 13, None),
    ("TIR Estado", "tir_est", 12, PCT2), ("VPN Estado @6.3%", "vpn_est_rest", 15, NUM),
    ("VPN Estado @9%", "vpn_est_9", 15, NUM), ("Año recupera", "rec", 12, "0"),
    ("Relicitación", "fee", 13, NUM), ("TIR desarrollo", "tir_dev", 13, PCT2)], RES["escenarios"])
tabla("Sensibilidad", "Sensibilidad sobre el caso base E4", [
    ("Variación", "nombre", 42, None), ("TIR inversionistas", "tir_inv", 15, PCT2), ("¿Cumple r_inv?", "inv_ok", 13, None),
    ("TIR Estado", "tir_est", 12, PCT2), ("VPN Estado @6.3%", "vpn_est_rest", 15, NUM), ("Año recupera", "rec", 12, "0")],
    RES["sensibilidad"])
tabla("Plazos", "Primer periodo mínimo (años) para que inversionistas y Estado cobren sus retornos", [
    ("Costo del capital", "r_inv", 16, PCT), ("T1 mínimo, Lima Moderna", "T1_min", 24, "0"),
    ("T1 mínimo, alquiler −20%", "T1_min_alq80", 24, "0")], RES["plazos"])

# ------------------------------------------------------------------ Asequibilidad (fórmulas)
A = wb.create_sheet("Asequibilidad")
A["A1"] = "Bono visible a la familia y brecha de pago (soles de t0, mensual)"; A["A1"].font = TITLE
bono = sp.BONO
ins = [("Bono mensual", bono["monto"], NUM, "Diseño de la Ley 30952 (Renta Joven); monto a verificar en su reglamento vigente"),
       ("Parte del bono que paga alquiler", bono["pct_alquiler"], PCT, "Resto va a cuenta de ahorro para la cuota inicial"),
       ("Años de bono", bono["anios"], "0", "Temporal: se espera graduación a Techo Propio / Nuevo Crédito Mivivienda"),
       ("Área del departamento", bono["area_unidad"], "0", "m2; producto de 1-2 dormitorios"),
       ("Esfuerzo máximo sobre el ingreso", bono["pct_ingreso"], PCT, "Estándar internacional de asequibilidad (30%)")]
for k, (lab, v, fmt, src) in enumerate(ins):
    i = 4 + k
    A.cell(i, 2, lab); c = A.cell(i, 3, v); c.font = BLUE; c.number_format = fmt; A.cell(i, 5, src)
A["B10"] = "Alquiler de mercado del departamento"; A["C10"] = f"={n('renta0')}/12*C7"; A["C10"].number_format = NUM
A["B11"] = "Bono aplicado al alquiler"; A["C11"] = "=C4*C5"; A["C11"].number_format = NUM
A["B12"] = "Ahorro acumulado en el periodo"; A["C12"] = "=C4*(1-C5)*12*C6"; A["C12"].number_format = NUM
A["B13"] = "Costo fiscal por hogar en el periodo"; A["C13"] = "=C4*12*C6"; A["C13"].number_format = NUM
A["C10"].font = GREEN
for j, h in enumerate(["Ingreso del hogar", "Paga al 30%", "Brecha sin bono", "Brecha con bono", "¿Cubre?"], 2):
    c = A.cell(15, j, h); c.font = BOLD; c.fill = HDR
for k, y in enumerate((2500, 3000, 3500, 4000, 4500)):
    i = 16 + k
    c = A.cell(i, 2, y); c.font = BLUE; c.number_format = NUM
    A.cell(i, 3, f"=B{i}*$C$8").number_format = NUM
    A.cell(i, 4, f"=$C$10-C{i}").number_format = NUM
    A.cell(i, 5, f"=D{i}-$C$11").number_format = NUM
    A.cell(i, 6, f'=IF(E{i}<=0,"Sí","No")')
A["B22"] = "Ingreso mínimo atendido con el bono"; A["C22"] = "=(C10-C11)/C8"; A["C22"].number_format = NUM
A["B23"] = ("Nota: el alquiler supone un edificio en ubicación tipo Lima Moderna (factor de alquiler en Supuestos). "
            "La alícuota del bono es visible en el presupuesto público y no altera el retorno del terreno.")
A.column_dimensions["B"].width = 40; A.column_dimensions["C"].width = 14
for col in "DEF":
    A.column_dimensions[col].width = 16

out = os.path.join(HERE, "memoria-suelo-publico.xlsx")
wb.save(out)
print("ok", out)
