"""
Modelo de viabilidad: vivienda para venta (BTS) vs. vivienda para renta (BTR) en Lima Moderna.

Reproducible y auditable. Ejecutar:  python3 modelo/modelo_multifamily.py
Genera: modelo/resultados.json y tablas en consola.

Convenciones
- Moneda: soles nominales (S/). Periodo: trimestre. t = 0 es la compra del terreno.
- Todas las cifras de costos y rentas se expresan por m2 vendible/arrendable y se escalan
  por el área del proyecto (5,500 m2, ~100 unidades de 55 m2).
- Análisis antes de Impuesto a la Renta (comparación a nivel proyecto/empresa; ver memoria).
- El IGV se modela explícitamente como flujo de caja (débito, crédito y saldo a favor).
- El terreno se paga 100% con capital (salvo la variante de nota puente), por lo que los
  flujos de capital sin terreno no dependen de su precio: el valor residual del terreno es
  el VAN de esos flujos a la tasa exigida, dividido entre (1 + alcabala).
"""
from __future__ import annotations
import copy, json, os
import numpy_financial as npf

# ---------------------------------------------------------------------------
# 1. SUPUESTOS BASE (ver memoria-de-calculo.md, sección 2, para fuentes)
# ---------------------------------------------------------------------------
BASE = dict(
    # Mercado (BCRP, Nota de Estudios 16-2026, IV trim. 2025, precios de oferta Urbania;
    # promedio simple de los 6 distritos de Lima Moderna)
    tc=3.41,                   # S/ por US$ (nov-2026)
    precio_oferta_usd=1868.0,  # US$/m2, incluye IGV
    renta_oferta_usd=119.3,    # US$/m2/año (precio/alquiler PER ~15.6)
    desc_cierre=0.04,          # descuento oferta -> cierre (precio y renta)
    g_precio=0.025, g_renta=0.025, g_costo=0.03, g_opex=0.03,  # crecimiento nominal anual
    area=5500.0,               # m2 vendibles/arrendables
    # Costos (sin IGV)
    cd_m2=2665.0,              # costo directo por m2 vendible (2,050/m2 techado x 1.30)
    ind_pct=0.12,              # indirectos (proyecto, licencias, supervisión, gerencia) s/ CD
    ind_gravado=0.80,          # parte de indirectos afecta a IGV
    cont_pct=0.05,             # contingencia s/ CD
    com_bts=0.04,              # gastos de venta BTS s/ venta neta de IGV
    ffe_m2=150.0,              # amoblado/equipamiento de amenities BTR
    mkt_btr_m2=20.0,           # comercialización inicial BTR
    alcabala=0.03,             # sobre el precio del terreno
    igv=0.18, igv_venta_ef=0.09,  # primera venta: base excluye terreno (50%)
    # Calendario (trimestres)
    q_lic=(1, 3), q_obra=(4, 10), ind_pre=0.30,
    # BTS
    q_ventas=(3, 14), pct_inicial=0.20, q_entrega=11,
    hurdle_bts=0.20,
    # Deuda de construcción (BTS y BTR)
    ltc=0.65, kd_obra=0.100, fee_obra=0.01,
    ltc_btr=0.55,              # el banco dimensiona el crédito de obra BTR a la toma del mini-perm
    # BTR operación
    ocup_leaseup={11: 0.25, 12: 0.50, 13: 0.75, 14: 0.90}, ocup_estab=0.95,
    incobrable=0.01,
    opex_m2=72.0,              # S/ por m2/año sin IGV (desglose en memoria)
    opex_fijo=0.60, opex_gravado=0.70,
    reserva_capex=0.02,        # % de ingreso efectivo
    regimen="A",               # A: gravado, IGV absorbido; B: exonerado (sin crédito);
                               # C: hipotético tasa 0% con devolución del IGV de obra (no neutral)
    r_u_btr=None,              # retorno no apalancado exigido; None = cap_salida + g_renta (Gordon)
    rera=False, rera_lag=2,    # recuperación anticipada IGV de obra (D.Leg. 973)
    prima_renta=0.0,           # prima operativa sobre renta de mercado
    cap_salida=0.065, costo_venta=0.015, q_salida=22,
    salida="cap",              # "cap": venta en bloque a NOI/cap; "unidades": venta por unidades
    desc_usado=0.07,           # descuento de unidad usada frente a nueva (venta por unidades)
    factor_absorcion=0.92,     # valor presente de vender en ~8 trimestres (demora media ~4.5 trim. al 9%)
    com_unidades=0.04,         # gastos de venta por unidades
    haircut_credito=0.25,      # descuento al saldo de IGV transferido con el vehículo
    # Mini-perm
    miniperm=True, q_refi=14, kd_mp=0.090, amort_mp=20, ltv_mp=0.60, dscr_mp=1.25,
    dy_mp=0.095, fee_mp=0.01,
    hurdle_btr=0.14,
    # Nota puente de terreno (variante)
    puente=False, puente_pct=0.45, kd_puente=0.12, q_puente_fin=4,
)

N_BTS = 16
N_BTR = 27  # se proyecta hasta 27 para el NOI prospectivo de salida (t=23..26)


def tq(r):
    return (1 + r) ** 0.25 - 1


def irr_a(cf):
    r = npf.irr(cf)
    return (1 + r) ** 4 - 1 if r == r else float("nan")


def npv_q(r_annual, cf):
    rq = tq(r_annual)
    return sum(c / (1 + rq) ** t for t, c in enumerate(cf))


def esc(g, t):
    return (1 + g) ** (t / 4)


def rng(a, b):
    return range(a, b + 1)


# ---------------------------------------------------------------------------
# 2. COSTOS DE DESARROLLO (comunes a ambos modelos)
# ---------------------------------------------------------------------------
def costos_desarrollo(p, n, btr):
    A = p["area"]; cd_tot = p["cd_m2"] * A
    o0, o1 = p["q_obra"]; l0, l1 = p["q_lic"]
    nobra = o1 - o0 + 1; nlic = l1 - l0 + 1
    cost = [0.0] * n; igv_in = [0.0] * n
    for t in range(n):
        c = 0.0; g = 0.0
        if l0 <= t <= l1:
            x = cd_tot * p["ind_pct"] * p["ind_pre"] / nlic * esc(p["g_costo"], t)
            c += x; g += x * p["ind_gravado"]
        if o0 <= t <= o1:
            e = esc(p["g_costo"], t)
            cd = cd_tot / nobra * e
            ind = cd_tot * p["ind_pct"] * (1 - p["ind_pre"]) / nobra * e
            cont = cd_tot * p["cont_pct"] / nobra * e
            c += cd + ind + cont; g += cd + cont + ind * p["ind_gravado"]
        if btr:
            if t in (o1 - 1, o1):
                x = p["ffe_m2"] * A / 2 * esc(p["g_costo"], t); c += x; g += x
            if t in (o1, o1 + 1, o1 + 2):
                x = p["mkt_btr_m2"] * A / 3 * esc(p["g_costo"], t); c += x; g += x
        cost[t] = c; igv_in[t] = g * p["igv"]
    return cost, igv_in


def deuda_obra(p, cf_u, cost_obra_incl_igv, n, q_fin=None, ltc=None):
    """Crédito de obra con barrido de caja. Desembolsa solo para cubrir déficits,
    hasta LTC x costo de obra (con IGV) de cada trimestre; intereses capitalizados.
    Si q_fin está dado, el saldo se cancela en ese trimestre (refinanciamiento)."""
    rq = tq(p["kd_obra"]); bal = 0.0
    ltc = p["ltc"] if ltc is None else ltc
    facility = ltc * sum(cost_obra_incl_igv)
    D = [0.0] * n; R = [0.0] * n; I = [0.0] * n; BAL = [0.0] * n; FEE = [0.0] * n
    FEE[p["q_obra"][0]] = p["fee_obra"] * facility
    for t in range(n):
        I[t] = bal * rq; bal += I[t]
        cf = cf_u[t] - FEE[t]
        if q_fin is not None and t >= q_fin:
            BAL[t] = bal if t == q_fin else 0.0
            if t == q_fin:
                R[t] = bal; bal = 0.0
            continue
        if cf < 0:
            D[t] = min(ltc * cost_obra_incl_igv[t], -cf)
        else:
            R[t] = min(bal, cf)
        bal += D[t] - R[t]; BAL[t] = bal
    return dict(D=D, R=R, I=I, BAL=BAL, FEE=FEE, facility=facility)


# ---------------------------------------------------------------------------
# 3. MODELO BTS (construir para vender)
# ---------------------------------------------------------------------------
def modelo_bts(p):
    n = N_BTS; A = p["area"]
    p0 = p["precio_oferta_usd"] * p["tc"] * (1 - p["desc_cierre"])  # S/ m2 con IGV
    s0, s1 = p["q_ventas"]; ns = s1 - s0 + 1
    contrato = [0.0] * n; cobro = [0.0] * n; com = [0.0] * n
    for t in rng(s0, s1):
        v = A / ns * p0 * esc(p["g_precio"], t)
        contrato[t] = v
        cobro[t] += v * p["pct_inicial"]
        cobro[max(t, p["q_entrega"])] += v * (1 - p["pct_inicial"])
        com[t] = v / (1 + p["igv_venta_ef"]) * p["com_bts"]
    cost, igv_in = costos_desarrollo(p, n, btr=False)
    igv_in = [igv_in[t] + com[t] * p["igv"] for t in range(n)]
    igv_out = [c * p["igv_venta_ef"] / (1 + p["igv_venta_ef"]) for c in cobro]
    cb = 0.0; igv_pag = [0.0] * n; CB = [0.0] * n
    for t in range(n):
        cb += igv_in[t]; use = min(cb, igv_out[t]); cb -= use
        igv_pag[t] = igv_out[t] - use; CB[t] = cb
    cf_u = [cobro[t] - cost[t] - com[t] - igv_in[t] - igv_pag[t] for t in range(n)]
    obra = [(cost[t] + igv_in[t]) if p["q_obra"][0] <= t <= p["q_obra"][1] else 0.0 for t in range(n)]
    d = deuda_obra(p, cf_u, obra, n)
    eq = [cf_u[t] - d["FEE"][t] + d["D"][t] - d["R"][t] for t in range(n)]
    eq[-1] -= d["BAL"][-1]  # cualquier saldo remanente lo cubre el capital
    hurd = p["hurdle_bts"]
    land_res = npv_q(hurd, eq) / (1 + p["alcabala"])
    land_res_u = npv_q(0.15, cf_u) / (1 + p["alcabala"])
    venta_neta = sum(cobro) / (1 + p["igv_venta_ef"])
    return dict(cobro=cobro, cost=cost, com=com, igv_in=igv_in, igv_out=igv_out,
                igv_pag=igv_pag, saldo_igv_final=CB[-1], cf_u=cf_u, deuda=d, eq=eq,
                venta_neta=venta_neta, land_res=land_res, land_res_u15=land_res_u,
                land_res_m2=land_res / A,
                incidencia=land_res / sum(cobro), p0=p0)


def flujos_con_terreno(eq, L, p, puente=False):
    """Agrega el terreno (y opcionalmente la nota puente) a los flujos de capital."""
    f = list(eq)
    f[0] -= L * (1 + p["alcabala"])
    if puente:
        B = p["puente_pct"] * L; f[0] += B
        f[p["q_puente_fin"]] -= B * (1 + p["kd_puente"]) ** (p["q_puente_fin"] / 4)
    return f


# ---------------------------------------------------------------------------
# 4. MODELO BTR (construir para rentar)
# ---------------------------------------------------------------------------
def modelo_btr(p):
    n = max(N_BTR, p["q_salida"] + 5); A = p["area"]; ig = p["igv"]; regA = p["regimen"] == "A"; regC = p["regimen"] == "C"
    r0 = p["renta_oferta_usd"] * p["tc"] * (1 - p["desc_cierre"]) * (1 + p["prima_renta"])
    o1 = p["q_obra"][1]
    occ = [0.0] * n
    for t in range(n):
        if t > o1:
            occ[t] = p["ocup_leaseup"].get(t, p["ocup_estab"]) if t <= max(p["ocup_leaseup"]) else p["ocup_estab"]
    renta_mkt = [A * r0 / 4 * esc(p["g_renta"], t) * occ[t] * (1 - p["incobrable"]) for t in range(n)]
    # Ingreso neto de IGV para el propietario
    ing = [r / (1 + ig) if regA else r for r in renta_mkt]
    igv_out = [x * ig if regA else 0.0 for x in ing]
    opex_stab = [A * p["opex_m2"] / 4 * esc(p["g_opex"], t) if t > o1 else 0.0 for t in range(n)]
    opex = [opex_stab[t] * (p["opex_fijo"] + (1 - p["opex_fijo"]) * occ[t] / p["ocup_estab"]) for t in range(n)]
    opex_igv = [o * p["opex_gravado"] * ig for o in opex]
    reserva = [p["reserva_capex"] * ing[t] for t in range(n)]
    # NOI: en régimen B el IGV de gastos es costo (no hay crédito)
    noi = [ing[t] - opex[t] - reserva[t] - (0.0 if (regA or regC) else opex_igv[t]) for t in range(n)]
    cost, igv_obra = costos_desarrollo(p, n, btr=True)
    # IGV: crédito (A) o costo (B)
    cb = 0.0; CB = [0.0] * n; igv_pag = [0.0] * n; refund = [0.0] * n
    for t in range(n):
        if regA:
            if p["rera"] and t <= o1:
                if t + p["rera_lag"] < n:
                    refund[t + p["rera_lag"]] += igv_obra[t]
                cb += opex_igv[t]
            else:
                cb += igv_obra[t] + opex_igv[t]
            use = min(cb, igv_out[t]); cb -= use; igv_pag[t] = igv_out[t] - use
        elif regC:  # devolución del IGV de obra y de gastos con rezago
            if t + p["rera_lag"] < n:
                refund[t + p["rera_lag"]] += igv_obra[t] + opex_igv[t]
        CB[t] = cb
    qs = p["q_salida"]
    noi_fwd = sum(noi[qs + 1: qs + 5])
    valor_salida = noi_fwd / p["cap_salida"]
    credito_transf = CB[qs] * (1 - p["haircut_credito"]) if regA else 0.0
    neto_salida = valor_salida * (1 - p["costo_venta"]) + credito_transf
    if p["salida"] == "unidades":
        pu = p["precio_oferta_usd"] * p["tc"] * (1 - p["desc_cierre"]) * esc(p["g_precio"], qs)
        bruto = A * pu * (1 - p["desc_usado"]) * p["factor_absorcion"]
        igv_exit = bruto * p["igv_venta_ef"] / (1 + p["igv_venta_ef"])
        valor_salida = bruto / (1 + p["igv_venta_ef"]) * (1 - p["com_unidades"])
        credito_transf = min(CB[qs], igv_exit) if regA else 0.0
        neto_salida = valor_salida + credito_transf
    # Flujo no apalancado (antes de IR). En régimen A el IGV de gastos se paga y luego
    # se recupera vía crédito; en B ya está dentro del NOI.
    cf_u = [0.0] * n
    for t in range(qs + 1):
        cf_u[t] = (renta_mkt[t] - opex[t] - reserva[t] - opex_igv[t] - cost[t] - igv_obra[t]
                   - igv_pag[t] + refund[t])
        # nota: renta_mkt incluye el IGV cobrado; igv_pag es lo que se entrega a SUNAT
    cf_u[qs] += neto_salida
    cf_u = cf_u[: qs + 1]
    obra = [(cost[t] + igv_obra[t]) if t <= o1 + 2 else 0.0 for t in range(qs + 1)]
    # Deuda
    q_refi = p["q_refi"] if p["miniperm"] else p["q_refi"]
    d = deuda_obra(p, cf_u[:], obra, qs + 1, q_fin=q_refi, ltc=p["ltc_btr"])
    eq = [0.0] * (qs + 1)
    mp = dict(monto=0.0, cuota=0.0, BAL=[0.0] * (qs + 1), DSCR=[None] * (qs + 1))
    for t in range(qs + 1):
        eq[t] = cf_u[t] - d["FEE"][t] + d["D"][t] - d["R"][t]
    if p["miniperm"]:
        noi_f = sum(noi[q_refi + 1: q_refi + 5]); v_refi = noi_f / p["cap_salida"]
        rq = tq(p["kd_mp"]); nper = p["amort_mp"] * 4
        cuota_q = rq / (1 - (1 + rq) ** -nper)  # por sol de préstamo
        k_anual = 4 * cuota_q
        lim = dict(LTV=p["ltv_mp"] * v_refi, DSCR=noi_f / (p["dscr_mp"] * k_anual), DY=noi_f / p["dy_mp"])
        L = min(lim.values()); cuota = L * cuota_q
        mp.update(monto=L, cuota=cuota, limites=lim, restriccion=min(lim, key=lim.get),
                  valor_refi=v_refi, noi_refi=noi_f, k_anual=k_anual)
        eq[q_refi] += L * (1 - p["fee_mp"])
        bal = L
        for t in range(q_refi + 1, qs + 1):
            interes = bal * rq; amort = cuota - interes; bal -= amort
            eq[t] -= cuota; mp["BAL"][t] = bal
            mp["DSCR"][t] = noi[t] / cuota
        mp["BAL"][q_refi] = L
        eq[qs] -= bal; mp["balloon"] = bal / L
    land_res = npv_q(p["hurdle_btr"], eq) / (1 + p["alcabala"])
    r_u = p["r_u_btr"] if p["r_u_btr"] is not None else p["cap_salida"] + p["g_renta"]
    land_res_u = npv_q(r_u, cf_u) / (1 + p["alcabala"])
    costo_total_sin_terreno = sum(cost) + (0.0 if (regA or regC) else sum(igv_obra))
    noi_estab_anual = sum(noi[15:19])
    return dict(reserva_ded=reserva, occ=occ, renta_mkt=renta_mkt, ing=ing, opex=opex, noi=noi, cost=cost,
                igv_obra=igv_obra, igv_pag=igv_pag, saldo_credito=CB, refund=refund,
                valor_salida=valor_salida, neto_salida=neto_salida, credito_transf=credito_transf,
                cf_u=cf_u, deuda=d, mp=mp, eq=eq, land_res=land_res, land_res_m2=land_res / A,
                land_res_u=land_res_u, land_res_u_m2=land_res_u / A,
                costo_total_sin_terreno=costo_total_sin_terreno, noi_estab_anual=noi_estab_anual,
                r0=r0)


# ---------------------------------------------------------------------------
# 5. EVALUACIÓN INTEGRADA
# ---------------------------------------------------------------------------
def evaluar(p, L_mercado=None):
    bts = modelo_bts(p); btr = modelo_btr(p)
    L = bts["land_res"] if L_mercado is None else L_mercado
    A = p["area"]
    f_btr_e = flujos_con_terreno(btr["eq"], L, p, p["puente"])
    f_btr_u = flujos_con_terreno(btr["cf_u"], L, p)
    f_bts_e = flujos_con_terreno(bts["eq"], L, p, p["puente"])
    f_bts_u = flujos_con_terreno(bts["cf_u"], L, p)
    costo_total = btr["costo_total_sin_terreno"] + L * (1 + p["alcabala"])
    yoc = btr["noi_estab_anual"] / costo_total
    return dict(
        L=L, L_m2=L / A,
        bts=dict(tir_eq=irr_a(f_bts_e), tir_u=irr_a(f_bts_u), land_res_m2=bts["land_res_m2"],
                 incidencia=bts["incidencia"], margen=(sum(f_bts_u) / (sum(bts["cost"]) + sum(bts["com"]) + L * (1 + p["alcabala"])))),
        btr=dict(tir_eq=irr_a(f_btr_e), tir_u=irr_a(f_btr_u), land_res_m2=btr["land_res_m2"],
                 yoc=yoc, cap=p["cap_salida"], spread_desarrollo_pb=(yoc - p["cap_salida"]) * 1e4,
                 noi_m2=btr["noi_estab_anual"] / A, mp_monto=btr["mp"]["monto"],
                 mp_restriccion=btr["mp"].get("restriccion"),
                 ltv_mp=btr["mp"]["monto"] / btr["mp"]["valor_refi"] if p["miniperm"] else 0.0,
                 dscr_min=min([x for x in btr["mp"]["DSCR"] if x], default=None),
                 balloon=btr["mp"].get("balloon"),
                 ratio_terreno=btr["land_res"] / bts["land_res"],
                 land_res_u_m2=btr["land_res_u_m2"], ratio_terreno_u=btr["land_res_u"] / bts["land_res"]),
        _bts=bts, _btr=btr, _f=dict(btr_e=f_btr_e, btr_u=f_btr_u, bts_e=f_bts_e, bts_u=f_bts_u),
    )


def var(**kw):
    p = copy.deepcopy(BASE); p.update(kw); return p


def escenarios():
    base = evaluar(BASE); Lm = base["L"]
    sc = [
        ("Base: alquiler gravado, IGV absorbido (régimen A)", {}),
        ("A + recuperación anticipada IGV (D.Leg. 973)", dict(rera=True)),
        ("Régimen B: alquiler exonerado (PL 58-2026)", dict(regimen="B")),
        ("Régimen C hipotético: tasa 0% con devolución (no neutral)", dict(regimen="C")),
        ("A + nota puente de terreno 45% al 12%", dict(puente=True)),
        ("A sin mini-perm (capital cancela obra en t=14)", dict(miniperm=False)),
        ("A con mini-perm solo interés (equivale a amortización muy larga)", dict(amort_mp=100)),
        ("A + financiamiento verde (-75 pb obra y mini-perm, +1% CD)", dict(kd_obra=0.0925, kd_mp=0.0825, cd_m2=BASE["cd_m2"] * 1.01)),
        ("A + construcción industrializada (-5% CD)", dict(cd_m2=BASE["cd_m2"] * 0.95)),
        ("A + prima operativa de renta +5%", dict(prima_renta=0.05)),
        ("A + cap de salida 6.00%", dict(cap_salida=0.060)),
        ("A + cap de salida 7.00%", dict(cap_salida=0.070)),
        ("A + vacancia estructural 8%", dict(ocup_estab=0.92)),
        ("A + opex +20%", dict(opex_m2=BASE["opex_m2"] * 1.2)),
        ("A con salida por venta de unidades a personas naturales", dict(salida="unidades")),
        ("B con salida por venta de unidades a personas naturales", dict(regimen="B", salida="unidades")),
        ("A con tenencia de 10 años (venta en t=50)", dict(q_salida=50)),
        ("B con tenencia de 10 años (venta en t=50)", dict(regimen="B", q_salida=50)),
        ("B + cap 6.00% + prima 5% (caso favorable)", dict(regimen="B", cap_salida=0.060, prima_renta=0.05)),
        ("A + RERA + puente + verde + industrializada (toda la ingeniería)", dict(
            rera=True, puente=True, kd_obra=0.0925, kd_mp=0.0825, cd_m2=BASE["cd_m2"] * 0.96)),
        ("B + toda la ingeniería + cap 6.00% + prima 5%", dict(
            regimen="B", puente=True, kd_obra=0.0925, kd_mp=0.0825, cd_m2=BASE["cd_m2"] * 0.96,
            cap_salida=0.060, prima_renta=0.05)),
    ]
    out = []
    for name, kw in sc:
        # el precio de mercado del terreno lo fija el BTS del caso base (no cambia con la
        # estructura del BTR), salvo que el cambio afecte también al BTS (costo de obra).
        afecta_bts = any(k in kw for k in ("cd_m2", "kd_obra"))
        p = var(**kw)
        r = evaluar(p, None if afecta_bts else Lm)
        out.append(dict(escenario=name, L_m2=r["L_m2"], **{f"btr_{k}": v for k, v in r["btr"].items()},
                        bts_tir_eq=r["bts"]["tir_eq"], bts_land_m2=r["bts"]["land_res_m2"]))
    # Casos de nicho: terreno a fracción del precio de mercado (aporte patrimonial / JV)
    for name, kw, f in [
        ("Nicho: B + prima 10% + cap 6.00% + terreno al 50%", dict(regimen="B", prima_renta=0.10, cap_salida=0.060), 0.5),
        ("Nicho: idem sin mini-perm", dict(regimen="B", prima_renta=0.10, cap_salida=0.060, miniperm=False), 0.5),
        ("Nicho: A + prima 10% + cap 6.00% + terreno al 50%", dict(prima_renta=0.10, cap_salida=0.060), 0.5),
        ("Nicho: B + prima 10% + cap 6.00% + terreno sin costo (aporte)", dict(regimen="B", prima_renta=0.10, cap_salida=0.060), 0.0),
        ("Nicho: B + prima 20% + cap 6.00% + terreno a mercado", dict(regimen="B", prima_renta=0.20, cap_salida=0.060), 1.0),
    ]:
        r = evaluar(var(**kw), Lm * f)
        out.append(dict(escenario=name, L_m2=r["L_m2"], **{f"btr_{k}": v for k, v in r["btr"].items()},
                        bts_tir_eq=r["bts"]["tir_eq"], bts_land_m2=r["bts"]["land_res_m2"]))
    return base, out


def sens_grid():
    """Ratio terreno residual BTR / BTS por cap de salida x régimen de IGV x prima."""
    g = []
    for reg in ("A", "B"):
        for prima in (0.0, 0.10, 0.20, 0.30):
            for cap in (0.055, 0.060, 0.065, 0.070, 0.075):
                r = evaluar(var(regimen=reg, prima_renta=prima, cap_salida=cap))
                g.append(dict(regimen=reg, prima=prima, cap=cap, ratio=r["btr"]["ratio_terreno"],
                              ratio_u=r["btr"]["ratio_terreno_u"],
                              btr_land_m2=r["btr"]["land_res_m2"], tir_eq=r["btr"]["tir_eq"],
                              tir_u=r["btr"]["tir_u"]))
    return g


def hurdle_equivalente(p=BASE):
    """TIR no apalancada y del capital del BTR según el precio del terreno
    (fracción del precio de mercado que fija el BTS)."""
    Lm = modelo_bts(BASE)["land_res"]; out = []
    for f in (0.0, 0.25, 0.50, 0.75, 1.0):
        r = evaluar(p, Lm * f)
        out.append(dict(fraccion=f, L_m2=Lm * f / p["area"], tir_u=r["btr"]["tir_u"],
                        tir_eq=r["btr"]["tir_eq"], yoc=r["btr"]["yoc"]))
    return out


def sens_bts():
    out = []
    for name, kw in [("Base", {}), ("Precio -5%", dict(precio_oferta_usd=BASE["precio_oferta_usd"] * 0.95)),
                     ("Ventas en 16 trimestres", dict(q_ventas=(3, 18))),
                     ("Hurdle BTS 18%", dict(hurdle_bts=0.18)), ("Hurdle BTS 22%", dict(hurdle_bts=0.22)),
                     ("CD +10%", dict(cd_m2=BASE["cd_m2"] * 1.10))]:
        p = var(**kw)
        if kw.get("q_ventas"):
            global N_BTS
            old = N_BTS; N_BTS = 20; b = modelo_bts(p); N_BTS = old
        else:
            b = modelo_bts(p)
        out.append(dict(caso=name, land_m2=b["land_res_m2"], incidencia=b["incidencia"]))
    return out


def despues_ir(p=BASE, L=None, tasa=0.295, dep=0.05):
    """Prueba de robustez: TIR no apalancada después de IR (29.5%) para BTS y BTR.
    Simplificaciones: pérdidas arrastrables sin límite; BTS reconoce la utilidad al
    cobrar el saldo; BTR deprecia 5% anual todo el costo de desarrollo (sin terreno)."""
    bts = modelo_bts(p); btr = modelo_btr(p)
    L = bts["land_res"] if L is None else L
    Lc = L * (1 + p["alcabala"])
    # BTS
    vn = bts["venta_neta"]; util = vn - sum(bts["cost"]) - sum(bts["com"]) - Lc - bts["saldo_igv_final"]
    rec = [c / (1 + p["igv_venta_ef"]) for c in bts["cobro"]]
    tax_b = [tasa * max(util, 0) * x / vn for x in rec]
    f_b = flujos_con_terreno(bts["cf_u"], L, p); f_b = [f_b[t] - tax_b[t] for t in range(len(f_b))]
    # BTR
    qs = p["q_salida"]; basis = sum(btr["cost"]) + (0 if p["regimen"] == "A" else sum(btr["igv_obra"]))
    o1 = p["q_obra"][1]; acc = 0.0; nol = 0.0; tax_r = []
    for t in range(qs + 1):
        d = basis * dep / 4 if t > o1 else 0.0
        acc += d
        ti = btr["noi"][t] + btr["reserva_ded"][t] - d if t > o1 else 0.0
        if t == qs:
            ti += btr["neto_salida"] - (basis - acc) - Lc
        ti -= nol; nol = 0.0
        if ti < 0: nol = -ti; ti = 0.0
        tax_r.append(tasa * ti)
    f_r = flujos_con_terreno(btr["cf_u"], L, p); f_r = [f_r[t] - tax_r[t] for t in range(len(f_r))]
    return dict(bts_tir_u_dir=irr_a(f_b), btr_tir_u_dir=irr_a(f_r))


DISTRITOS = [  # BCRP NE 16-2026, IV-2025: US$/m2 precio, US$/m2/año alquiler
    ("Surquillo", 1849, 128), ("Pueblo Libre", 1717, 115), ("Lince", 1970, 132),
    ("Magdalena", 1880, 116), ("Jesús María", 2086, 125), ("San Miguel", 1697, 100),
]


def prima_equilibrio(reg, cap, estricta=False, lo=0.0, hi=1.5):
    """Prima de renta sobre el promedio de Lima Moderna con la que el BTR paga el terreno de mercado (ratio = 1)."""
    k = "ratio_terreno" if estricta else "ratio_terreno_u"
    f = lambda x: evaluar(var(regimen=reg, prima_renta=x, cap_salida=cap))["btr"][k] - 1.0
    if f(lo) >= 0:
        return lo
    if f(hi) < 0:
        return None
    for _ in range(40):
        m = (lo + hi) / 2
        if f(m) >= 0:
            hi = m
        else:
            lo = m
    return hi


def sens_renta():
    """Prima de renta de equilibrio y renta implícita (US$/m2/año de oferta), por régimen, cap y vara."""
    out = []
    for reg in ("A", "B"):
        for cap in (0.060, 0.065):
            for estricta in (False, True):
                x = prima_equilibrio(reg, cap, estricta)
                out.append(dict(regimen=reg, cap=cap, vara="estricta 14%" if estricta else "laxa 9%",
                                prima=x, renta_usd=None if x is None else BASE["renta_oferta_usd"] * (1 + x)))
    return out


def sens_distritos():
    out = []
    for nm, pr, rt in DISTRITOS:
        for reg in ("A", "B"):
            r = evaluar(var(precio_oferta_usd=pr, renta_oferta_usd=rt, regimen=reg))
            out.append(dict(distrito=nm, per=pr / rt, regimen=reg, L_m2=r["L_m2"], yoc=r["btr"]["yoc"],
                            tir_u=r["btr"]["tir_u"], ratio_u=r["btr"]["ratio_terreno_u"]))
    return out


def inversionista_individual(p=BASE):
    """Rendimiento del comprador persona natural que alquila (benchmark de demanda)."""
    precio = p["precio_oferta_usd"] * p["tc"] * (1 - p["desc_cierre"])  # con IGV, por m2
    costos_compra = 0.015  # notaría, registros, alcabala sobre terreno (aprox., ver memoria)
    renta = p["renta_oferta_usd"] * p["tc"] * (1 - p["desc_cierre"])
    vac = 0.08; corretaje = 0.5 / 12; predial = 0.002 * precio; mant_vacio = 0.08 * 0.12 * renta
    ir = 0.05 * renta * (1 - vac)
    neto = renta * (1 - vac) - renta * corretaje - predial - mant_vacio - ir
    y_bruto = renta / precio; y_neto = neto / (precio * (1 + costos_compra))
    # TIR a 10 años con apreciación igual a g_precio y venta con 3% de costos
    cf = [-precio * (1 + costos_compra)] + [neto * (1 + p["g_renta"]) ** k for k in range(10)]
    cf[-1] += precio * (1 + p["g_precio"]) ** 10 * 0.97
    return dict(y_bruto=y_bruto, y_neto=y_neto, tir_10a=npf.irr(cf))


if __name__ == "__main__":
    base, sc = escenarios()
    b, r = base["_bts"], base["_btr"]
    A = BASE["area"]
    print("=== CASO BASE ===")
    print(f"Precio cierre BTS S/{b['p0']:,.0f}/m2 (con IGV); renta cierre BTR S/{r['r0']:,.0f}/m2/año (con IGV si gravado)")
    print(f"Terreno residual BTS (hurdle {BASE['hurdle_bts']:.0%}): S/{b['land_res_m2']:,.0f}/m2 vendible; incidencia {b['incidencia']:.1%} de ventas")
    print(f"Terreno residual BTR (hurdle {BASE['hurdle_btr']:.0%}): S/{r['land_res_m2']:,.0f}/m2 -> ratio {base['btr']['ratio_terreno']:.2f}")
    print(f"BTS TIR equity {base['bts']['tir_eq']:.1%} | TIR no apalancada {base['bts']['tir_u']:.1%}")
    print(f"BTR con terreno a precio de mercado: TIR equity {base['btr']['tir_eq']:.1%} | no apalancada {base['btr']['tir_u']:.1%}")
    print(f"BTR NOI estab. S/{base['btr']['noi_m2']:,.0f}/m2/año; YoC {base['btr']['yoc']:.2%} vs cap {BASE['cap_salida']:.2%}")
    print(f"Mini-perm: S/{r['mp']['monto']/A:,.0f}/m2, restricción {r['mp']['restriccion']}, LTV {base['btr']['ltv_mp']:.0%}, DSCR mín {base['btr']['dscr_min']:.2f}x, balloon {r['mp']['balloon']:.0%}")
    print(f"Terreno residual BTR no apalancado (r = cap + g = 9.0%): S/{r['land_res_u_m2']:,.0f}/m2 -> ratio {base['btr']['ratio_terreno_u']:.2f}")
    for h in hurdle_equivalente():
        print(f"  terreno al {h['fraccion']:.0%} del mercado (S/{h['L_m2']:,.0f}/m2): TIR u {h['tir_u']:.1%}  TIR eq {h['tir_eq']:.1%}  YoC {h['yoc']:.2%}")
    print("\n=== ESCENARIOS (terreno a precio de mercado BTS base salvo nota) ===")
    for s in sc:
        print(f"{s['escenario'][:62]:62} TIR eq {s['btr_tir_eq']:6.1%} TIR u {s['btr_tir_u']:6.1%} DSCRmin {s['btr_dscr_min'] or 0:4.2f} YoC {s['btr_yoc']:5.2%} ratio terreno {s['btr_ratio_terreno']:.2f}")
    print("\n=== MAPA: ratio terreno BTR/BTS ===")
    grid = sens_grid()
    for gg in grid:
        print(f"  ratio no apalancado {gg['ratio_u']:.2f} |", end=" ")
        print(f"reg {gg['regimen']} prima {gg['prima']:.0%} cap {gg['cap']:.2%}: ratio {gg['ratio']:.2f}  TIR eq {gg['tir_eq']:.1%}")
    print("\n=== BTS sensibilidad ===")
    sb = sens_bts()
    for x in sb: print(x)
    ind = inversionista_individual(); print("\nInversionista individual:", ind)
    dir_ = {k: despues_ir(var(**kw)) for k, kw in [("A", {}), ("B", dict(regimen="B")), ("A_unidades", dict(salida="unidades"))]}
    print("Después de IR:", dir_)
    dist = sens_distritos()
    sr = sens_renta()
    for x in sr: print('prima equilibrio', x)
    for d in dist: print(d)
    res = dict(supuestos={k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()}) for k, v in BASE.items()},
               base={k: v for k, v in base.items() if not k.startswith("_")},
               escenarios=sc, mapa=grid, bts_sens=sb, individual=ind, despues_ir=dir_, distritos=dist, sens_renta=sr,
               terreno_fraccion=hurdle_equivalente(),
               flujos=dict(bts_eq=base["_f"]["bts_e"], btr_eq=base["_f"]["btr_e"],
                           btr_u=base["_f"]["btr_u"], bts_u=base["_f"]["bts_u"]))
    with open(os.path.join(os.path.dirname(__file__), "resultados.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=float, ensure_ascii=False)
