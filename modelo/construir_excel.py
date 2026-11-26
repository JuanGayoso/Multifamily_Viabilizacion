"""Genera modelo/memoria-de-calculo.xlsx con fórmulas vivas que replican modelo_multifamily.py.
Ejecutar: python3 modelo/construir_excel.py  (luego recalcular con LibreOffice)."""
import json, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.comments import Comment
from modelo_multifamily import BASE

HERE = os.path.dirname(os.path.abspath(__file__))
RES = json.load(open(os.path.join(HERE, "resultados.json")))

F = "Arial"
BLUE = Font(name=F, color="0000FF"); BLACK = Font(name=F); GREEN = Font(name=F, color="008000")
BOLD = Font(name=F, bold=True); TITLE = Font(name=F, bold=True, size=13)
HDR = PatternFill("solid", fgColor="DDEBF7"); YEL = PatternFill("solid", fgColor="FFFF00")
NUM = '#,##0;(#,##0);"-"'; PCT = '0.0%;(0.0%);"-"'; PCT2 = '0.00%;(0.00%);"-"'; X = '0.00"x"'

wb = Workbook()

# ---------------------------------------------------------------- Léeme
ws = wb.active; ws.title = "Leeme"
lines = [
    ("Memoria de cálculo: vivienda para venta (BTS) vs. vivienda para renta (BTR), Lima Moderna", TITLE),
    ("Réplica en fórmulas del script modelo/modelo_multifamily.py (mismo repositorio).", None),
    ("", None),
    ("Cómo usar", BOLD),
    ("1. Los supuestos editables están en la hoja Supuestos en azul; los clave, con fondo amarillo.", None),
    ("2. Las hojas BTS y BTR calculan flujos trimestrales (t = 0 es la compra del terreno).", None),
    ("3. Resumen muestra los resultados y los compara con el script de Python (control).", None),
    ("4. Escenarios y Mapa son tablas de valores generadas por el script (no se recalculan aquí).", None),
    ("", None),
    ("Convenciones", BOLD),
    ("Soles nominales. Cifras de proyecto de 5,500 m2 vendibles (~100 departamentos de 55 m2).", None),
    ("Antes de Impuesto a la Renta. IGV modelado como flujo de caja.", None),
    ("Azul = dato ingresado · Negro = fórmula · Verde = vínculo a otra hoja.", None),
    ("Limitación: la hoja admite trimestre de salida hasta 22 (columnas hasta t = 26).", None),
    ("Régimen de IGV: A = alquiler gravado con IGV absorbido; B = alquiler exonerado sin crédito fiscal;", None),
    ("C = hipotético tasa 0% con devolución (se incluye solo para medir su costo; no es neutral).", None),
]
for i, (t, f) in enumerate(lines, 1):
    c = ws.cell(i, 1, t); c.font = f or BLACK
ws.column_dimensions["A"].width = 110

# ---------------------------------------------------------------- Supuestos
S = wb.create_sheet("Supuestos")
S["A1"] = "Supuestos (valores base al 25-nov-2026)"; S["A1"].font = TITLE
for j, h in enumerate(["Parámetro", "Valor", "Unidad", "Fuente / sustento"], 1):
    c = S.cell(3, j + 1, h); c.font = BOLD; c.fill = HDR
rows = [
    # name, label, value, unit, source, fmt, key
    ("sec", "Mercado", None, None, None, None, False),
    ("tc", "Tipo de cambio", BASE["tc"], "S/ por US$", "BCRP, tipo de cambio interbancario, mediados de nov-2026 (~3.40-3.41)", "0.00", False),
    ("precio_usd", "Precio de oferta departamentos Lima Moderna", BASE["precio_oferta_usd"], "US$/m2 (con IGV)", "BCRP, Nota de Estudios 16-2026 (IV trim. 2025), mediana Urbania, sector de ingresos medios", NUM, True),
    ("renta_usd", "Alquiler de oferta Lima Moderna", BASE["renta_oferta_usd"], "US$/m2/año", "BCRP, Nota de Estudios 16-2026: promedio simple de Jesús María 125, Lince 132, Magdalena 116, Pueblo Libre 115, San Miguel 100, Surquillo 128", "0.0", True),
    ("desc", "Descuento oferta a cierre (precio y renta)", BASE["desc_cierre"], "%", "Estimación; se aplica igual a ambos modelos para no sesgar la comparación", PCT, False),
    ("gp", "Crecimiento nominal precio", BASE["g_precio"], "% anual", "Estimación: inflación de largo plazo ~2.5% (meta BCRP 2% ±1; BBVA Research 2.2% a dic-2027); sin crecimiento real", PCT, False),
    ("gr", "Crecimiento nominal renta", BASE["g_renta"], "% anual", "Ídem", PCT, False),
    ("gc", "Crecimiento costo de construcción", BASE["g_costo"], "% anual", "Estimación (índices de materiales INEI; verificar)", PCT, False),
    ("go", "Crecimiento opex", BASE["g_opex"], "% anual", "Estimación", PCT, False),
    ("area", "Área vendible / arrendable", BASE["area"], "m2", "Proyecto ilustrativo: 100 departamentos de 55 m2", NUM, False),
    ("sec", "Costos (sin IGV)", None, None, None, None, False),
    ("cd", "Costo directo por m2 vendible", BASE["cd_m2"], "S/ por m2", "S/ 2,050 por m2 techado sin IGV (≈S/ 2,420 con IGV) x 1.30 m2 techado/vendible. Rango de mercado S/ 1,800-3,800 por m2 techado; verificar con CAPECO/presupuestos", NUM, True),
    ("ind", "Indirectos sobre costo directo", BASE["ind_pct"], "%", "Proyecto, licencias, supervisión, gerencia, seguros, legal; práctica de mercado 10-15%", PCT, False),
    ("indg", "Parte de indirectos afecta a IGV", BASE["ind_gravado"], "%", "Estimación (tasas municipales y planillas no llevan IGV)", PCT, False),
    ("cont", "Contingencia sobre costo directo", BASE["cont_pct"], "%", "Práctica de mercado", PCT, False),
    ("com", "Gastos de venta BTS", BASE["com_bts"], "% de venta neta", "Comisiones, marketing, sala de ventas; práctica 3-5%", PCT, False),
    ("ffe", "Amoblado y amenities BTR", BASE["ffe_m2"], "S/ por m2", "Estimación", NUM, False),
    ("mkt", "Comercialización inicial BTR", BASE["mkt_btr_m2"], "S/ por m2", "Estimación", NUM, False),
    ("alc", "Alcabala sobre terreno", BASE["alcabala"], "%", "Ley de Tributación Municipal (D.Leg. 776), 3% (tramo inafecto de 10 UIT no considerado)", PCT, False),
    ("igv", "Tasa IGV (incl. IPM)", BASE["igv"], "%", "TUO Ley del IGV", PCT, False),
    ("igvef", "IGV efectivo en primera venta", BASE["igv_venta_ef"], "%", "Base excluye el terreno, presumido en 50% del precio (Ley del IGV, art. 13 / reglamento); 18% x 50%", PCT, False),
    ("sec", "Calendario (trimestres)", None, None, None, None, False),
    ("l0", "Inicio licencias", BASE["q_lic"][0], "t", "Estimación", "0", False),
    ("l1", "Fin licencias", BASE["q_lic"][1], "t", "Estimación (9 meses)", "0", False),
    ("o0", "Inicio obra", BASE["q_obra"][0], "t", "", "0", False),
    ("o1", "Fin obra", BASE["q_obra"][1], "t", "21 meses de obra", "0", False),
    ("indpre", "Parte de indirectos antes de obra", BASE["ind_pre"], "%", "Estimación", PCT, False),
    ("sec", "BTS", None, None, None, None, False),
    ("s0", "Inicio ventas", BASE["q_ventas"][0], "t", "Lanzamiento en preventa", "0", False),
    ("s1", "Fin ventas", BASE["q_ventas"][1], "t", "Absorción ~8 unidades por trimestre", "0", False),
    ("ini", "Cuota inicial cobrada al vender", BASE["pct_inicial"], "%", "Práctica: 10-30%; saldo con hipotecario a la entrega", PCT, False),
    ("ent", "Trimestre de entrega", BASE["q_entrega"], "t", "", "0", False),
    ("hbts", "TIR exigida al capital BTS", BASE["hurdle_bts"], "% anual", "Opinión profesional: promotores exigen 18-25% en soles", PCT, True),
    ("sec", "Deuda de construcción", None, None, None, None, False),
    ("ltc", "LTC crédito promotor BTS (sobre costo de obra con IGV)", BASE["ltc"], "%", "Práctica de mercado 60-70%", PCT, False),
    ("ltcb", "LTC crédito de obra BTR", BASE["ltc_btr"], "%", "Dimensionado a la toma del mini-perm", PCT, False),
    ("kdo", "Tasa crédito de obra", BASE["kd_obra"], "TEA", "Supuesto: soberano 10 años ~6.1% + ~390 pb; tasa activa de medianas empresas por verificar en SBS", PCT, True),
    ("feeo", "Comisión de estructuración obra", BASE["fee_obra"], "% de la línea", "Práctica", PCT, False),
    ("sec", "BTR operación", None, None, None, None, False),
    ("oc11", "Ocupación t=11", BASE["ocup_leaseup"][11], "%", "Colocación ~8 unidades/mes", PCT, False),
    ("oc12", "Ocupación t=12", BASE["ocup_leaseup"][12], "%", "", PCT, False),
    ("oc13", "Ocupación t=13", BASE["ocup_leaseup"][13], "%", "", PCT, False),
    ("oc14", "Ocupación t=14", BASE["ocup_leaseup"][14], "%", "", PCT, False),
    ("ocs", "Ocupación estabilizada", BASE["ocup_estab"], "%", "Vacancia estructural 5% (FIBRA Prime: 95.3% de ocupación en activos comerciales)", PCT, True),
    ("inc", "Incobrables", BASE["incobrable"], "% de renta", "Estimación", PCT, False),
    ("opex", "Opex del propietario", BASE["opex_m2"], "S/ por m2/año sin IGV", "Desglose en memoria: administración 16, predial y arbitrios 22, seguros 8, rotación 7, reparaciones 8, áreas comunes no recuperables 6, otros 5", NUM, True),
    ("opf", "Parte fija del opex", BASE["opex_fijo"], "%", "Estimación", PCT, False),
    ("opg", "Parte del opex afecta a IGV", BASE["opex_gravado"], "%", "Estimación", PCT, False),
    ("res", "Reserva de reposición", BASE["reserva_capex"], "% de ingreso", "Metodología de tasación (contrato 11)", PCT, False),
    ("reg", "Régimen IGV (A, B o C)", BASE["regimen"], "", "A: vigente (alquiler por empresa gravado; IGV absorbido para competir con arrendador persona natural)", None, True),
    ("rera", "Recuperación anticipada IGV (1 = sí)", 0, "", "D.Leg. 973: requiere inversión ≥ US$5M y etapa preproductiva ≥ 2 años", "0", False),
    ("lag", "Rezago de devolución", BASE["rera_lag"], "trimestres", "Estimación", "0", False),
    ("prima", "Prima operativa sobre renta de mercado", BASE["prima_renta"], "%", "Base 0%: no hay serie pública que la respalde", PCT, True),
    ("cap", "Cap rate de salida (NOI)", BASE["cap_salida"], "%", "Soberano 10 años ~6.1% + prima inmobiliaria ~2.9% - crecimiento 2.5% (Gordon)", PCT2, True),
    ("cv", "Costos de venta en la salida", BASE["costo_venta"], "%", "Práctica", PCT, False),
    ("qs", "Trimestre de venta (máx. 22 en esta hoja)", BASE["q_salida"], "t", "2 años tras estabilizar", "0", False),
    ("hc", "Descuento al saldo de IGV transferido", BASE["haircut_credito"], "%", "Estimación del valor presente para el comprador", PCT, False),
    ("sec", "Mini-perm", None, None, None, None, False),
    ("mp", "Mini-perm activo (1 = sí)", 1, "", "", "0", False),
    ("qr", "Trimestre de refinanciamiento", BASE["q_refi"], "t", "", "0", False),
    ("kdm", "Tasa mini-perm", BASE["kd_mp"], "TEA", "Supuesto: soberano ~6.1% + ~290 pb", PCT, True),
    ("am", "Amortización", BASE["amort_mp"], "años", "Perfil de 20 años", "0", False),
    ("ltvm", "LTV máximo", BASE["ltv_mp"], "%", "", PCT, False),
    ("dscr", "DSCR mínimo", BASE["dscr_mp"], "x", "", X, False),
    ("dy", "Debt yield mínimo", BASE["dy_mp"], "%", "", PCT, False),
    ("feem", "Comisión mini-perm", BASE["fee_mp"], "%", "", PCT, False),
    ("hbtr", "TIR exigida al capital BTR", BASE["hurdle_btr"], "% anual", "Opinión profesional: 12-16% para desarrollo con estabilización", PCT, True),
    ("sec", "Nota puente de terreno", None, None, None, None, False),
    ("pu", "Nota puente activa (1 = sí)", 0, "", "", "0", False),
    ("pupct", "Porcentaje del terreno financiado", BASE["puente_pct"], "%", "", PCT, False),
    ("kdp", "Tasa nota puente", BASE["kd_puente"], "TEA", "Fondos de deuda privada (estimación)", PCT, False),
    ("qp", "Trimestre de cancelación", BASE["q_puente_fin"], "t", "", "0", False),
    ("sec", "Derivados", None, None, None, None, False),
    ("p0", "Precio de cierre BTS", "=precio_usd*tc*(1-desc)", "S/ por m2 con IGV", "", NUM, False),
    ("r0", "Renta de cierre BTR", "=renta_usd*tc*(1-desc)*(1+prima)", "S/ por m2/año", "", NUM, False),
    ("cdt", "Costo directo total", "=cd*area", "S/", "", NUM, False),
    ("nobra", "Trimestres de obra", "=o1-o0+1", "", "", "0", False),
    ("nlic", "Trimestres de licencias", "=l1-l0+1", "", "", "0", False),
    ("nven", "Trimestres de venta", "=s1-s0+1", "", "", "0", False),
    ("rqo", "Tasa trimestral obra", "=(1+kdo)^0.25-1", "", "", "0.000%", False),
    ("rqm", "Tasa trimestral mini-perm", "=(1+kdm)^0.25-1", "", "", "0.000%", False),
    ("ru", "Retorno no apalancado exigido BTR", "=cap+gr", "% anual", "Gordon: cap + g", PCT2, False),
]
N = {}
r = 4
for name, label, val, unit, src, fmt, key in rows:
    if name == "sec":
        S.cell(r, 2, label).font = BOLD; r += 1; continue
    N[name] = f"Supuestos!$C${r}"
    S.cell(r, 2, label).font = BLACK
    r += 1
# second pass to write values with resolved names
r = 4
import re
def sub(expr):
    def rep(m):
        w = m.group(0)
        return N[w].replace("Supuestos!", "") if w in N else w
    return re.sub(r"[A-Za-z_][A-Za-z0-9_]*", rep, expr)
for name, label, val, unit, src, fmt, key in rows:
    if name == "sec":
        r += 1; continue
    c = S.cell(r, 3)
    if isinstance(val, str) and val.startswith("="):
        c.value = sub(val); c.font = BLACK
    else:
        c.value = val; c.font = BLUE
    if key: c.fill = YEL
    if fmt: c.number_format = fmt
    S.cell(r, 4, unit).font = BLACK; S.cell(r, 5, src).font = BLACK
    r += 1
for col, w in zip("ABCDE", (2, 52, 14, 22, 120)):
    S.column_dimensions[col].width = w


def n(name):
    return N[name]


def fx(expr):
    """Reemplaza nombres de supuestos por referencias absolutas."""
    def rep(m):
        w = m.group(0)
        return N[w] if w in N else w
    return re.sub(r"\b[a-z][a-z0-9_]*\b", rep, expr)


# ---------------------------------------------------------------- helpers de hoja de flujos
def sheet_flows(title, T):
    w = wb.create_sheet(title)
    w["A1"] = title; w["A1"].font = TITLE
    w.cell(3, 1, "Concepto").font = BOLD; w.cell(3, 2, "Unidad").font = BOLD
    for t in range(T):
        c = w.cell(3, 3 + t, t); c.font = BOLD; c.fill = HDR; c.alignment = Alignment(horizontal="center")
        w.column_dimensions[L(3 + t)].width = 11.5
    w.column_dimensions["A"].width = 46; w.column_dimensions["B"].width = 12
    w.freeze_panes = "C4"
    return w


def row(w, r, label, unit, f, T, fmt=NUM, font=BLACK, bold=False):
    """f(col_letter, prev_col_letter, t_index) -> fórmula"""
    w.cell(r, 1, label).font = BOLD if bold else BLACK; w.cell(r, 2, unit).font = BLACK
    for t in range(T):
        col = L(3 + t); prev = L(2 + t)
        c = w.cell(r, 3 + t, f(col, prev, t)); c.number_format = fmt; c.font = font


# ---------------------------------------------------------------- BTS
TB = 16
B = sheet_flows("BTS", TB)
last = L(2 + TB)
tr = lambda c: f"{c}$3"
R = {}
def br(r, key, label, unit, f, fmt=NUM, bold=False):
    R[key] = r; row(B, r, label, unit, f, TB, fmt, bold=bold)

br(4, "ec", "Escalamiento de costos", "índice", lambda c, p, t: fx(f"=(1+gc)^({tr(c)}/4)"), "0.0000")
br(5, "ep", "Escalamiento de precios", "índice", lambda c, p, t: fx(f"=(1+gp)^({tr(c)}/4)"), "0.0000")
br(6, "fv", "Trimestre de venta (1/0)", "", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=s0,{tr(c)}<=s1),1,0)"), "0")
br(7, "ct", "Ventas contratadas (con IGV)", "S/", lambda c, p, t: fx(f"={c}6*area/nven*p0*{c}5"))
br(8, "ci", "Cobro cuota inicial", "S/", lambda c, p, t: fx(f"={c}7*ini"))
br(9, "cs", "Cobro saldo (a la entrega o al vender)", "S/", lambda c, p, t: fx(
    f"=IF({tr(c)}<ent,0,IF({tr(c)}=ent,SUMPRODUCT(($C$3:${last}$3<=ent)*$C$7:${last}$7),{c}7)*(1-ini))"))
br(10, "co", "Cobranza total (con IGV)", "S/", lambda c, p, t: f"={c}8+{c}9", bold=True)
br(11, "cm", "Gastos de venta", "S/", lambda c, p, t: fx(f"={c}7/(1+igvef)*com"))
br(12, "ip", "Indirectos antes de obra", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=l0,{tr(c)}<=l1),cdt*ind*indpre/nlic*{c}4,0)"))
br(13, "cd", "Costo directo", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=o0,{tr(c)}<=o1),cdt/nobra*{c}4,0)"))
br(14, "io", "Indirectos de obra", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=o0,{tr(c)}<=o1),cdt*ind*(1-indpre)/nobra*{c}4,0)"))
br(15, "cn", "Contingencia", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=o0,{tr(c)}<=o1),cdt*cont/nobra*{c}4,0)"))
br(16, "ctot", "Costo de desarrollo (sin IGV)", "S/", lambda c, p, t: f"=SUM({c}12:{c}15)", bold=True)
br(17, "gin", "IGV pagado en compras (crédito)", "S/", lambda c, p, t: fx(f"=igv*({c}12*indg+{c}13+{c}15+{c}14*indg+{c}11)"))
br(18, "gout", "IGV de ventas (débito)", "S/", lambda c, p, t: fx(f"={c}10*igvef/(1+igvef)"))
br(19, "gcb", "Saldo de crédito fiscal (fin)", "S/", lambda c, p, t: (f"={c}17-MIN({c}17,{c}18)" if t == 0 else f"={p}19+{c}17-MIN({p}19+{c}17,{c}18)"))
br(20, "gpag", "IGV pagado a SUNAT", "S/", lambda c, p, t: (f"={c}18-MIN({c}17,{c}18)" if t == 0 else f"={c}18-MIN({p}19+{c}17,{c}18)"))
br(21, "cfu", "Flujo no apalancado sin terreno", "S/", lambda c, p, t: f"={c}10-{c}16-{c}11-{c}17-{c}20", bold=True)
br(22, "ob", "Costo de obra con IGV (base LTC)", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=o0,{tr(c)}<=o1),{c}16+{c}17,0)"))
br(23, "fee", "Comisión de estructuración", "S/", lambda c, p, t: fx(f"=IF({tr(c)}=o0,feeo*ltc*SUM($C$22:${last}$22),0)"))
br(24, "int", "Interés capitalizado", "S/", lambda c, p, t: ("=0" if t == 0 else fx(f"={p}28*rqo")))
br(25, "cfn", "Flujo neto de comisión", "S/", lambda c, p, t: f"={c}21-{c}23")
br(26, "des", "Desembolso crédito promotor", "S/", lambda c, p, t: fx(f"=IF({c}25<0,MIN(ltc*{c}22,-{c}25),0)"))
br(27, "rep", "Repago (barrido de caja)", "S/", lambda c, p, t: ("=0" if t == 0 else f"=IF({c}25>=0,MIN({p}28+{c}24,{c}25),0)"))
br(28, "bal", "Saldo crédito promotor", "S/", lambda c, p, t: (f"={c}26-{c}27" if t == 0 else f"={p}28+{c}24+{c}26-{c}27"))
br(29, "eq", "Flujo del capital sin terreno", "S/", lambda c, p, t: (f"={c}25+{c}26-{c}27" + (f"-{c}28" if t == TB - 1 else "")), bold=True)
br(30, "equ", "Flujo del capital con terreno de mercado", "S/", lambda c, p, t: (
    f"={c}29-Resumen!$C$6*(1+{n('alc')})+IF({n('pu')}=1,{n('pupct')}*Resumen!$C$6,0)" if t == 0 else
    fx(f"={c}29-IF(AND(pu=1,{tr(c)}=qp),pupct*Resumen!$C$6*(1+kdp)^(qp/4),0)")), bold=True)
br(31, "cfuu", "Flujo no apalancado con terreno de mercado", "S/", lambda c, p, t: (
    f"={c}21-Resumen!$C$6*(1+{n('alc')})" if t == 0 else f"={c}21"))

# ---------------------------------------------------------------- BTR
TR = 27
W = sheet_flows("BTR", TR)
lr = L(2 + TR)
def rr(r, label, unit, f, fmt=NUM, bold=False):
    row(W, r, label, unit, f, TR, fmt, bold=bold)
rr(4, "Escalamiento de costos", "índice", lambda c, p, t: fx(f"=(1+gc)^({tr(c)}/4)"), "0.0000")
rr(5, "Escalamiento de renta", "índice", lambda c, p, t: fx(f"=(1+gr)^({tr(c)}/4)"), "0.0000")
rr(6, "Escalamiento de opex", "índice", lambda c, p, t: fx(f"=(1+go)^({tr(c)}/4)"), "0.0000")
rr(7, "Ocupación", "%", lambda c, p, t: fx(
    f"=IF({tr(c)}<=o1,0,IF({tr(c)}=11,oc11,IF({tr(c)}=12,oc12,IF({tr(c)}=13,oc13,IF({tr(c)}=14,oc14,ocs)))))"), PCT)
rr(8, "Renta cobrada al inquilino (precio de mercado)", "S/", lambda c, p, t: fx(f"=area*r0/4*{c}5*{c}7*(1-inc)"))
rr(9, "Ingreso del propietario neto de IGV", "S/", lambda c, p, t: fx(f'=IF(reg="A",{c}8/(1+igv),{c}8)'))
rr(10, "IGV de alquileres (débito)", "S/", lambda c, p, t: fx(f'=IF(reg="A",{c}9*igv,0)'))
rr(11, "Opex estabilizado", "S/", lambda c, p, t: fx(f"=IF({tr(c)}>o1,area*opex/4*{c}6,0)"))
rr(12, "Opex", "S/", lambda c, p, t: fx(f"={c}11*(opf+(1-opf)*{c}7/ocs)"))
rr(13, "IGV de opex", "S/", lambda c, p, t: fx(f"={c}12*opg*igv"))
rr(14, "Reserva de reposición", "S/", lambda c, p, t: fx(f"=res*{c}9"))
rr(15, "NOI", "S/", lambda c, p, t: fx(f'={c}9-{c}12-{c}14-IF(reg="B",{c}13,0)'), bold=True)
rr(16, "Indirectos antes de obra", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=l0,{tr(c)}<=l1),cdt*ind*indpre/nlic*{c}4,0)"))
rr(17, "Costo directo", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=o0,{tr(c)}<=o1),cdt/nobra*{c}4,0)"))
rr(18, "Indirectos de obra", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=o0,{tr(c)}<=o1),cdt*ind*(1-indpre)/nobra*{c}4,0)"))
rr(19, "Contingencia", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=o0,{tr(c)}<=o1),cdt*cont/nobra*{c}4,0)"))
rr(20, "Amoblado y amenities", "S/", lambda c, p, t: fx(f"=IF(OR({tr(c)}=o1-1,{tr(c)}=o1),ffe*area/2*{c}4,0)"))
rr(21, "Comercialización inicial", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>=o1,{tr(c)}<=o1+2),mkt*area/3*{c}4,0)"))
rr(22, "Costo de desarrollo (sin IGV)", "S/", lambda c, p, t: f"=SUM({c}16:{c}21)", bold=True)
rr(23, "IGV de obra", "S/", lambda c, p, t: fx(f"=igv*({c}16*indg+{c}17+{c}19+{c}18*indg+{c}20+{c}21)"))
rr(24, "Adición al crédito fiscal", "S/", lambda c, p, t: fx(f'=IF(reg="A",IF(AND(rera=1,{tr(c)}<=o1),{c}13,{c}23+{c}13),0)'))
rr(25, "Uso del crédito fiscal", "S/", lambda c, p, t: (fx(f'=IF(reg="A",MIN({c}24,{c}10),0)') if t == 0 else fx(f'=IF(reg="A",MIN({p}26+{c}24,{c}10),0)')))
rr(26, "Saldo de crédito fiscal (fin)", "S/", lambda c, p, t: (f"={c}24-{c}25" if t == 0 else f"={p}26+{c}24-{c}25"))
rr(27, "IGV pagado a SUNAT", "S/", lambda c, p, t: f"={c}10-{c}25")
rr(28, "Devolución de IGV (D.Leg. 973 o régimen C)", "S/", lambda c, p, t: fx(
    f'=IF({tr(c)}<lag,0,IF(AND(reg="A",rera=1),IF({tr(c)}-lag<=o1,INDEX($C$23:${lr}$23,{tr(c)}-lag+1),0),IF(reg="C",INDEX($C$23:${lr}$23,{tr(c)}-lag+1)+INDEX($C$13:${lr}$13,{tr(c)}-lag+1),0)))'))
rr(29, "Flujo operativo y de desarrollo", "S/", lambda c, p, t: f"={c}8-{c}12-{c}14-{c}13-{c}22-{c}23-{c}27+{c}28")
# salida (celdas de resumen en la hoja BTR, columna B filas 50+)
W["A48"] = "Salida"; W["A48"].font = BOLD
W["A49"] = "NOI prospectivo (4 trimestres posteriores a la venta)"; W["C49"] = fx(f"=SUMPRODUCT(($C$3:${lr}$3>qs)*($C$3:${lr}$3<=qs+4)*$C$15:${lr}$15)")
W["A50"] = "Valor de salida (NOI / cap)"; W["C50"] = fx("=C49/cap")
W["A51"] = "Saldo de crédito fiscal transferido (con descuento)"; W["C51"] = fx(f'=IF(reg="A",INDEX($C$26:${lr}$26,qs+1)*(1-hc),0)')
W["A52"] = "Ingreso neto de la salida"; W["C52"] = fx("=C50*(1-cv)+C51")
for rr_ in range(49, 53): W.cell(rr_, 3).number_format = NUM
rr(30, "Flujo no apalancado sin terreno", "S/", lambda c, p, t: fx(f"=IF({tr(c)}<=qs,{c}29+IF({tr(c)}=qs,$C$52,0),0)"), bold=True)
rr(31, "Costo de obra con IGV (base LTC)", "S/", lambda c, p, t: fx(f"=IF({tr(c)}<=o1+2,{c}22+{c}23,0)"))
rr(32, "Comisión de estructuración", "S/", lambda c, p, t: fx(f"=IF({tr(c)}=o0,feeo*ltcb*SUMPRODUCT(($C$3:${lr}$3<=qs)*$C$31:${lr}$31),0)"))
rr(33, "Interés capitalizado", "S/", lambda c, p, t: ("=0" if t == 0 else fx(f"={p}36*rqo")))
rr(34, "Desembolso crédito de obra", "S/", lambda c, p, t: fx(f"=IF({tr(c)}>=qr,0,IF({c}30-{c}32<0,MIN(ltcb*{c}31,-({c}30-{c}32)),0))"))
rr(35, "Repago crédito de obra", "S/", lambda c, p, t: ("=0" if t == 0 else fx(f"=IF({tr(c)}=qr,{p}36+{c}33,IF({tr(c)}>qr,0,IF({c}30-{c}32>=0,MIN({p}36+{c}33,{c}30-{c}32),0)))")))
rr(36, "Saldo crédito de obra", "S/", lambda c, p, t: (f"={c}34-{c}35" if t == 0 else f"={p}36+{c}33+{c}34-{c}35"))
W["A54"] = "Mini-perm"; W["A54"].font = BOLD
mp_rows = [
    (55, "NOI prospectivo al refinanciar", f"=SUMPRODUCT(($C$3:${lr}$3>qr)*($C$3:${lr}$3<=qr+4)*$C$15:${lr}$15)", NUM),
    (56, "Valor al refinanciar (NOI / cap)", "=C55/cap", NUM),
    (57, "Cuota trimestral por sol prestado", "=rqm/(1-(1+rqm)^(-am*4))", "0.00000"),
    (58, "Constante anual de servicio", "=4*C57", PCT2),
    (59, "Límite por LTV", "=ltvm*C56", NUM),
    (60, "Límite por DSCR", "=C55/(dscr*C58)", NUM),
    (61, "Límite por debt yield", "=C55/dy", NUM),
    (62, "Monto del mini-perm", "=IF(mp=1,MIN(C59:C61),0)", NUM),
    (63, "Cuota trimestral", "=C62*C57", NUM),
    (64, "LTV resultante", "=IF(C56>0,C62/C56,0)", PCT),
]
for r_, lab, f, fmt in mp_rows:
    W.cell(r_, 1, lab).font = BLACK; c = W.cell(r_, 3, fx(f)); c.number_format = fmt
rr(37, "Desembolso mini-perm (neto de comisión)", "S/", lambda c, p, t: fx(f"=IF({tr(c)}=qr,$C$62*(1-feem),0)"))
rr(38, "Servicio de deuda mini-perm", "S/", lambda c, p, t: fx(f"=IF(AND({tr(c)}>qr,{tr(c)}<=qs),$C$63,0)"))
rr(39, "Saldo mini-perm", "S/", lambda c, p, t: ("=0" if t == 0 else fx(f"=IF({tr(c)}>qs,0,IF({tr(c)}<qr,0,IF({tr(c)}=qr,$C$62,{p}39*(1+rqm)-$C$63)))")))
rr(40, "Cancelación en la venta", "S/", lambda c, p, t: fx(f"=IF({tr(c)}=qs,{c}39,0)"))
rr(41, "DSCR", "x", lambda c, p, t: f'=IF({c}38>0,{c}15/{c}38,"")', X)
rr(42, "Flujo del capital sin terreno", "S/", lambda c, p, t: fx(f"=IF({tr(c)}<=qs,{c}30-{c}32+{c}34-{c}35+{c}37-{c}38-{c}40,0)"), bold=True)
rr(43, "Flujo del capital con terreno de mercado", "S/", lambda c, p, t: (
    f"={c}42-Resumen!$C$6*(1+{n('alc')})+IF({n('pu')}=1,{n('pupct')}*Resumen!$C$6,0)" if t == 0 else
    fx(f"={c}42-IF(AND(pu=1,{tr(c)}=qp),pupct*Resumen!$C$6*(1+kdp)^(qp/4),0)")), bold=True)
rr(44, "Flujo no apalancado con terreno de mercado", "S/", lambda c, p, t: (
    f"={c}30-Resumen!$C$6*(1+{n('alc')})" if t == 0 else f"={c}30"), bold=True)

# ---------------------------------------------------------------- Resumen
X_ = wb.create_sheet("Resumen", 1)
X_["A1"] = "Resumen de resultados (caso según hoja Supuestos)"; X_["A1"].font = TITLE
hdr = ["Indicador", "Excel (fórmula)", "Python (caso base)", "Diferencia", "Nota"]
for j, h in enumerate(hdr, 1):
    c = X_.cell(3, j, h); c.font = BOLD; c.fill = HDR
bq = f"BTS!$C$3:${last}$3"; wq = f"BTR!$C$3:${lr}$3"
pb = RES["base"]
res_rows = [
    (4, "Terreno residual BTS (capital a TIR exigida)", fx(f"=SUMPRODUCT(BTS!$C$29:${last}$29/(1+hbts)^({bq}/4))/(1+alc)"), pb["L"], NUM, "Precio de mercado del terreno: lo fija el comprador BTS"),
    (5, "Terreno residual BTS por m2 vendible", "=C4/" + n("area"), pb["L_m2"], NUM, ""),
    (6, "Precio de terreno usado (= residual BTS)", "=C4", pb["L"], NUM, "Se puede sobrescribir para probar otro precio"),
    (7, "Incidencia del terreno sobre ventas BTS", f"=C4/SUM(BTS!$C$10:${last}$10)", pb["bts"]["incidencia"], PCT, "Referencia de mercado: 12-20% (opinión)"),
    (8, "TIR del capital BTS", f"=(1+IRR(BTS!$C$30:${last}$30))^4-1", pb["bts"]["tir_eq"], PCT, "Debe igualar la TIR exigida"),
    (9, "TIR no apalancada BTS", f"=(1+IRR(BTS!$C$31:${last}$31))^4-1", pb["bts"]["tir_u"], PCT, ""),
    (11, "NOI estabilizado BTR (t = 15 a 18)", f"=SUMPRODUCT(({wq}>=15)*({wq}<=18)*BTR!$C$15:${lr}$15)", pb["btr"]["noi_m2"] * BASE["area"], NUM, ""),
    (12, "Costo total BTR con terreno", fx(f'=SUM(BTR!$C$22:${lr}$22)+IF(reg="B",SUM(BTR!$C$23:${lr}$23),0)+C6*(1+alc)'), None, NUM, "En régimen B el IGV de obra es costo"),
    (13, "Rendimiento sobre costo (YoC)", "=C11/C12", pb["btr"]["yoc"], PCT2, "Comparar con cap de salida"),
    (14, "Cap de salida", "=" + n("cap"), BASE["cap_salida"], PCT2, ""),
    (15, "Margen de desarrollo (YoC - cap), pb", "=(C13-C14)*10000", pb["btr"]["spread_desarrollo_pb"], "0", "Negativo = el edificio vale menos de lo que cuesta"),
    (16, "TIR no apalancada BTR", f"=(1+IRR(BTR!$C$44:${lr}$44,0))^4-1", pb["btr"]["tir_u"], PCT, "Exigida: cap + g"),
    (17, "TIR del capital BTR", f"=(1+IRR(BTR!$C$43:${lr}$43,0))^4-1", pb["btr"]["tir_eq"], PCT, "Exigida: hoja Supuestos"),
    (18, "Terreno residual BTR (capital a TIR exigida)", fx(f"=SUMPRODUCT(BTR!$C$42:${lr}$42/(1+hbtr)^({wq}/4))/(1+alc)"), pb["btr"]["land_res_m2"] * BASE["area"], NUM, ""),
    (19, "Terreno residual BTR no apalancado (r = cap + g)", fx(f"=SUMPRODUCT(BTR!$C$30:${lr}$30/(1+ru)^({wq}/4))/(1+alc)"), pb["btr"]["land_res_u_m2"] * BASE["area"], NUM, ""),
    (20, "Ratio terreno BTR / BTS (no apalancado)", "=C19/C4", pb["btr"]["ratio_terreno_u"], "0.00", "≥ 1 significa que el BTR puede pagar el terreno de mercado"),
    (21, "Monto mini-perm", "=BTR!C62", pb["btr"]["mp_monto"], NUM, ""),
    (22, "LTV del mini-perm", "=BTR!C64", pb["btr"]["ltv_mp"], PCT, ""),
    (23, "DSCR mínimo", f"=MIN(BTR!$C$41:${lr}$41)", pb["btr"]["dscr_min"], X, ""),
    (24, "Balloon / monto inicial", "=IF(BTR!C62>0,INDEX(BTR!$C$39:$" + lr + "$39," + n("qs") + "+1)/BTR!C62,0)", pb["btr"]["balloon"], PCT, ""),
]
for r_, lab, f, pyv, fmt, note in res_rows:
    X_.cell(r_, 1, lab).font = BLACK
    f = re.sub(r"(?<![!$A-Z])C(\d+)\b", r"B\1", f)
    c = X_.cell(r_, 2, f); c.number_format = fmt
    if pyv is not None:
        X_.cell(r_, 3, pyv).number_format = fmt; X_.cell(r_, 3).font = BLUE
        d = X_.cell(r_, 4, f"=B{r_}-C{r_}"); d.number_format = fmt
    X_.cell(r_, 5, note).font = BLACK
X_["B6"] = "=B4"  # precio usado
# referencias de las hojas de flujos a Resumen!C6 -> usar columna B (Excel)
X_["A26"] = "Control: la columna Diferencia debe ser ~0 con los supuestos base. Si cambias supuestos, la columna Python ya no aplica."
X_["A26"].font = Font(name=F, italic=True)
for col, w in zip("ABCDE", (52, 18, 18, 14, 60)):
    X_.column_dimensions[col].width = w
# las hojas de flujos usan Resumen!$C$6; reapuntar a $B$6
for wsx in (B, W):
    for rowc in wsx.iter_rows():
        for c in rowc:
            if isinstance(c.value, str) and "Resumen!$C$6" in c.value:
                c.value = c.value.replace("Resumen!$C$6", "Resumen!$B$6")

# ---------------------------------------------------------------- Individual
I = wb.create_sheet("Individual")
I["A1"] = "Benchmark: persona natural que compra un departamento para alquilarlo (por m2)"; I["A1"].font = TITLE
ind = [
    (3, "Precio de compra (con IGV)", "=" + n("p0"), NUM, ""),
    (4, "Costos de compra", 0.015, PCT, "Notaría, registros y alcabala sobre la parte de terreno (estimación; verificar)"),
    (5, "Renta anual de mercado", fx("=renta_usd*tc*(1-desc)"), NUM, ""),
    (6, "Vacancia", 0.08, PCT, "Arrendador individual: rotación sin gestión profesional (estimación)"),
    (7, "Corretaje (meses de renta por año)", 0.5, "0.0", "Estimación"),
    (8, "Predial (% del precio)", 0.002, PCT2, "Tramos bajos del impuesto predial (0.2% hasta 15 UIT de autoavalúo)"),
    (9, "Mantenimiento durante vacancia (% de renta mensual)", 0.12, PCT, "Estimación"),
    (10, "IR de primera categoría (% de renta cobrada)", 0.05, PCT, "6.25% sobre 80% de la renta (art. 52-A LIR)"),
    (12, "Ingreso neto anual", "=B5*(1-B6)-B5*B7/12-B8*B3-B6*B9*B5-B10*B5*(1-B6)", NUM, ""),
    (13, "Rendimiento bruto", "=B5/B3", PCT2, ""),
    (14, "Rendimiento neto sobre inversión total", "=B12/(B3*(1+B4))", PCT2, ""),
    (15, "TIR a 10 años con apreciación = crecimiento de precios", None, PCT2, "Ver fila 18"),
]
for r_, lab, v, fmt, note in ind:
    I.cell(r_, 1, lab).font = BLACK
    if v is not None:
        c = I.cell(r_, 2, v); c.number_format = fmt; c.font = BLUE if not (isinstance(v, str) and v.startswith("=")) else BLACK
    I.cell(r_, 3, note).font = BLACK
I["A17"] = "Año"; I["A18"] = "Flujo"
for k in range(11):
    I.cell(17, 2 + k, k)
    if k == 0:
        I.cell(18, 2, "=-B3*(1+B4)")
    else:
        f = f"=$B$12*(1+{n('gr')})^{k-1}"
        if k == 10: f += f"+$B$3*(1+{n('gp')})^10*0.97"
        I.cell(18, 2 + k, f)
    I.cell(18, 2 + k).number_format = NUM
I["B15"] = "=IRR(B18:L18)"; I["B15"].number_format = PCT2
I.column_dimensions["A"].width = 52; I.column_dimensions["C"].width = 70

# ---------------------------------------------------------------- Escenarios (valores)
E = wb.create_sheet("Escenarios")
E["A1"] = "Escenarios (valores calculados por modelo_multifamily.py; no se recalculan aquí)"; E["A1"].font = TITLE
cols = [("escenario", "Escenario", None), ("L_m2", "Terreno usado S/ por m2", NUM), ("btr_yoc", "YoC", PCT2),
        ("btr_spread_desarrollo_pb", "YoC - cap (pb)", "0"), ("btr_tir_u", "TIR no apalancada", PCT),
        ("btr_tir_eq", "TIR del capital", PCT), ("btr_ltv_mp", "LTV mini-perm", PCT), ("btr_dscr_min", "DSCR mínimo", X),
        ("btr_ratio_terreno_u", "Ratio terreno BTR/BTS (no apalancado)", "0.00")]
for j, (_, h, _) in enumerate(cols, 1):
    c = E.cell(3, j, h); c.font = BOLD; c.fill = HDR
for i, s in enumerate(RES["escenarios"], 4):
    for j, (k, _, fmt) in enumerate(cols, 1):
        v = s.get(k); c = E.cell(i, j, v if v == v else None); c.font = BLACK
        if fmt: c.number_format = fmt
E.column_dimensions["A"].width = 70
for j in range(2, 10): E.column_dimensions[L(j)].width = 16

M = wb.create_sheet("Mapa")
M["A1"] = "Mapa de viabilidad: ratio terreno residual BTR (no apalancado, r = cap + 2.5%) / terreno BTS"; M["A1"].font = TITLE
M["A2"] = "≥ 1.00: el BTR puede pagar el precio de mercado del terreno. Valores del script Python."
caps = sorted({g["cap"] for g in RES["mapa"]})
r_ = 4
for reg in ("A", "B"):
    M.cell(r_, 1, f"Régimen {reg}").font = BOLD
    for j, cp in enumerate(caps, 2):
        c = M.cell(r_, j, cp); c.number_format = PCT2; c.font = BOLD; c.fill = HDR
    r_ += 1
    for prima in sorted({g["prima"] for g in RES["mapa"]}):
        M.cell(r_, 1, f"Prima de renta {prima:.0%}")
        for j, cp in enumerate(caps, 2):
            g = next(x for x in RES["mapa"] if x["regimen"] == reg and x["prima"] == prima and x["cap"] == cp)
            c = M.cell(r_, j, g["ratio_u"]); c.number_format = "0.00"
            if g["ratio_u"] >= 1: c.fill = PatternFill("solid", fgColor="C6EFCE")
        r_ += 1
    r_ += 1
M.column_dimensions["A"].width = 26

D = wb.create_sheet("Distritos")
D["A1"] = "Sensibilidad por distrito (precio y alquiler de oferta BCRP NE 16-2026; mismos costos). Valores del script Python."; D["A1"].font = TITLE
for j, h in enumerate(["Distrito", "PER", "Régimen IGV", "Terreno BTS S/ por m2", "YoC BTR", "TIR no apalancada BTR", "Ratio terreno BTR/BTS"], 1):
    c = D.cell(3, j, h); c.font = BOLD; c.fill = HDR
for i, d in enumerate(RES["distritos"], 4):
    for j, (k, fmt) in enumerate([("distrito", None), ("per", "0.0"), ("regimen", None), ("L_m2", NUM), ("yoc", PCT2), ("tir_u", PCT), ("ratio_u", "0.00")], 1):
        c = D.cell(i, j, d[k])
        if fmt: c.number_format = fmt
D.column_dimensions["A"].width = 16
for j in range(2, 8): D.column_dimensions[L(j)].width = 20
T_ = wb.create_sheet("DespuesIR")
T_["A1"] = "Prueba de robustez después de IR (29.5%), TIR no apalancada con terreno de mercado. Valores del script Python."; T_["A1"].font = TITLE
for i, (k, v) in enumerate(RES["despues_ir"].items(), 3):
    T_.cell(i, 1, {"A": "Régimen A, venta en bloque", "B": "Régimen B, venta en bloque", "A_unidades": "Régimen A, venta por unidades"}[k])
    T_.cell(i, 2, v["bts_tir_u_dir"]).number_format = PCT; T_.cell(i, 3, v["btr_tir_u_dir"]).number_format = PCT
T_["B2"] = "BTS"; T_["C2"] = "BTR"; T_.column_dimensions["A"].width = 40

out = os.path.join(HERE, "memoria-de-calculo.xlsx")
wb.save(out); print("ok", out)
