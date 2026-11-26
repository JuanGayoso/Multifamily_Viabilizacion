"""
Modelo del artículo 2: vivienda en renta sobre suelo público en derecho de superficie.

Pregunta: ¿puede un edificio BTR sobre suelo del Estado pagar a sus inversionistas y
devolver al Estado el valor de su terreno, sin subsidio al modelo de negocio?

Mecánica (anual, S/ por m2 vendible, soles nominales):
  1. El Estado aporta el terreno en derecho de superficie por T1 años. Se valora al precio
     de mercado (residual BTS del modelo del artículo 1).
  2. Cascada: el flujo del proyecto paga primero a los inversionistas hasta su retorno
     (r_inv); luego al Estado hasta recuperar el terreno con r_est; el excedente se reparte.
  3. Al final de T1 el edificio revierte al Estado sin pago, y el Estado licita un segundo
     periodo de T2 años. El nuevo operador paga al Estado el valor de ese periodo.
  4. La vivienda asequible se financia con un bono visible a la familia (modelo Ley 30952),
     no con el terreno.

Todos los supuestos de costo, alquiler y opex salen de BASE (modelo del artículo 1).
"""
import json
import os

import modelo_multifamily as m1

B = m1.BASE
AQUI = os.path.dirname(os.path.abspath(__file__))

SP = dict(
    regimen="B",          # paridad del IGV: alquiler de vivienda exonerado (estándar CO/CL)
    r_inv=0.075,          # costo combinado del capital por etapas (supuesto clave)
    r_est=0.063,          # costo de financiamiento del Estado (bono soberano 10 años en soles)
    T1=45,                # primer periodo del derecho de superficie (mínimo con holgura; ver plazo_minimo)
    T2=30,                # segundo periodo (relicitación)
    split=0.50,           # reparto del excedente sobre ambos retornos: fracción al Estado
    desc_renta=0.0,       # descuento sobre el alquiler de mercado cobrado al inquilino
    f_renta=1.0,          # factor de alquiler de la ubicación (1.0 = Lima Moderna)
    f_costo=1.0,          # factor de costo de construcción
    f_relic=1.0,          # factor sobre el valor de la relicitación
    sched=(0.15, 0.50, 0.35),   # desembolso de obra en los años 1, 2 y 3
    ocup=(0.0, 0.60),     # ocupación en los años 3 y 4; desde el año 5, ocup_estab
    renov=((20, 0.10), (35, 0.10)),  # renovaciones mayores (año, % del costo)
    renov_relic=0.15,     # renovación que asume el nuevo operador al relicitar
    r_lp=0.070,           # retorno del inversionista de largo plazo que compra en el año 5
    t_venta=5,            # año de venta del derecho de superficie estabilizado
)


def costos_base(p=B):
    """Costo de desarrollo sin terreno (sin IGV) e IGV de obra, por m2 vendible, precios de t0."""
    cd = p["cd_m2"]
    ind = cd * p["ind_pct"]
    cont = cd * p["cont_pct"]
    extra = p["ffe_m2"] + p["mkt_btr_m2"]
    costo = cd + ind + cont + extra
    gravado = cd + cont + ind * p["ind_gravado"] + extra
    return dict(cd=cd, ind=ind, cont=cont, extra=extra, costo=costo, igv_obra=gravado * p["igv"])


def renta_base(p=B):
    """Alquiler de cierre por m2 vendible al año, t0 (US$ de oferta × TC × (1 − descuento de cierre))."""
    return p["renta_oferta_usd"] * p["tc"] * (1 - p["desc_cierre"])


def terreno_mercado():
    """Valor de mercado del terreno: residual BTS del modelo del artículo 1 (S/ por m2 vendible)."""
    return m1.evaluar(m1.BASE)["L_m2"]


def proyecto(s=SP, p=B, L=None):
    s = dict(SP, **s) if s is not SP else SP
    L = terreno_mercado() if L is None else L
    c = costos_base(p)
    costo = c["costo"] * s["f_costo"]
    igv_obra = c["igv_obra"] * s["f_costo"]
    capex_base = costo + (igv_obra if s["regimen"] == "B" else 0.0)  # en B el IGV de obra es costo
    renta0 = renta_base(p) * s["f_renta"] * (1 - s["desc_renta"])
    oe = p["ocup_estab"]
    n = s["T1"] + s["T2"]
    gr, gc = p["g_renta"], p["g_costo"]
    fil = []
    credito = 0.0  # saldo de IGV a favor (solo régimen A)
    for t in range(n + 1):
        d = dict(t=t)
        d["obra"] = -capex_base * s["sched"][t - 1] * (1 + gc) ** t if 1 <= t <= 3 else 0.0
        if t == 3:
            occ = s["ocup"][0]
        elif t == 4:
            occ = s["ocup"][1]
        elif t >= 5:
            occ = oe
        else:
            occ = 0.0
        d["ocup"] = occ
        # renta0 es el alquiler por m2 alquilado; se cobra solo sobre la fracción ocupada (igual que el artículo 1)
        bruto = renta0 * (1 + gr) ** t * occ * (1 - p["incobrable"])
        d["renta"] = bruto if s["regimen"] == "B" else bruto / (1 + p["igv"])
        op = p["opex_m2"] * (1 + p["g_opex"]) ** t * (p["opex_fijo"] + (1 - p["opex_fijo"]) * occ / oe) if occ > 0 else 0.0
        igv_op = op * p["opex_gravado"] * p["igv"]
        d["opex"] = -(op + (igv_op if s["regimen"] == "B" else 0.0))
        d["reserva"] = -p["reserva_capex"] * d["renta"]
        d["noi"] = d["renta"] + d["opex"] + d["reserva"]
        ren = [x for (a, x) in s["renov"] if a == t and a <= s["T1"] - 3]  # no en los 2 últimos años: la asume la relicitación
        d["renov"] = -ren[0] * costo * (1 + gc) ** t if ren else 0.0
        d["igv_neto"] = 0.0
        fil.append(d)
    # Nota régimen A: la renta neta ya excluye el IGV (renta/1.18). El inversionista paga el IGV
    # de obra y opex y lo recupera conforme hay débito. Flujo de IGV del año = −IGV pagado + crédito usado.
    if s["regimen"] == "A":
        credito = 0.0
        for d in fil:
            t = d["t"]
            pag = 0.0
            if 1 <= t <= 3:
                pag += igv_obra * s["sched"][t - 1] * (1 + gc) ** t
            op = -d["opex"]
            pag += op * p["opex_gravado"] * p["igv"]
            credito += pag
            deb = d["renta"] * p["igv"]
            uso = min(deb, credito)
            credito -= uso
            d["igv_neto"] = -pag + uso
    T1 = s["T1"]
    for d in fil:
        d["cf"] = (d["obra"] + d["noi"] + d["renov"] + d["igv_neto"]) if d["t"] <= T1 else 0.0
    # Valor de la relicitación (pagado al Estado en T1)
    fee = sum(fil[t]["noi"] / (1 + s["r_inv"]) ** (t - T1) for t in range(T1 + 1, T1 + s["T2"] + 1))
    fee -= s["renov_relic"] * costo * (1 + gc) ** T1
    fee *= s["f_relic"]
    # Cascada
    bi, be = 0.0, L
    for d in fil:
        t = d["t"]
        if t > 0:
            bi *= 1 + s["r_inv"]
            be *= 1 + s["r_est"]
        d["bi_pre"], d["be_pre"] = bi, be
        cf = d["cf"]
        fi = fe = 0.0
        if t == 0:
            fe = -L
        if cf < 0:
            bi += -cf
            fi += cf
        else:
            a = min(cf, bi); bi -= a
            b = min(cf - a, be); be -= b
            ex = cf - a - b
            fi += a + ex * (1 - s["split"])
            fe += b + ex * s["split"]
        if t == T1:
            fe += fee
        d["f_inv"], d["f_est"], d["bi"], d["be"] = fi, fe, bi, be
    f_inv = [d["f_inv"] for d in fil[:T1 + 1]]
    f_est = [d["f_est"] for d in fil[:T1 + 1]]
    cfp = [d["cf"] for d in fil[:T1 + 1]]
    rec = next((d["t"] for d in fil[:T1 + 1] if d["be"] <= 1e-6 and d["t"] > 0), None)
    if rec is None and fil[T1]["be_pre"] > 0 and fee >= fil[T1]["be"]:
        rec = T1
    # Etapa de desarrollo: vende el derecho de superficie estabilizado en t_venta al inversionista de largo plazo
    tv = s["t_venta"]
    precio = sum(f_inv[t] / (1 + s["r_lp"]) ** (t - tv) for t in range(tv + 1, T1 + 1))
    f_dev = f_inv[:tv + 1]
    f_dev[tv] += precio
    out = dict(
        L=L, costo=costo, igv_obra=igv_obra, capex_base=capex_base, renta0=renta0, fee=fee,
        tir_proy=irr(cfp), tir_inv=irr(f_inv), inv_ok=fil[T1]["bi"] <= 1e-6,
        tir_est=irr(f_est), vpn_est_rest=npv(f_est, s["r_est"]), vpn_est_9=npv(f_est, 0.09),
        rec=rec, precio_lp=precio, tir_dev=irr(f_dev),
        yoc=fil[6]["noi"] / (capex_base * sum(s["sched"])) if T1 >= 6 else None,
    )
    return out, fil


def irr(cf):
    def f(r):
        return sum(c / (1 + r) ** i for i, c in enumerate(cf))
    lo, hi = -0.5, 1.0
    if f(lo) * f(hi) > 0:
        return float("nan")
    for _ in range(300):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return mid


def npv(cf, r):
    return sum(c / (1 + r) ** i for i, c in enumerate(cf))


def var(**kw):
    return dict(SP, **kw)


ESCENARIOS = [
    ("E0", "Referencia: IGV actual, capital 9%, 30 años", dict(regimen="A", r_inv=0.09, T1=30)),
    ("E1", "Paridad IGV, capital 9%, 45 años", dict(r_inv=0.09)),
    ("E2", "Paridad IGV, capital 8%, 45 años", dict(r_inv=0.08)),
    ("E3", "Paridad IGV, capital por etapas 7.5%, 40 años (equilibrio)", dict(T1=40)),
    ("E4", "Propuesta: paridad IGV, capital por etapas 7.5%, 45 años", dict()),
    ("E5", "Paridad IGV, capital 7.5%, 50 años", dict(T1=50)),
    ("E6", "E4 con descuento de 15% financiado con el terreno (no recomendado)", dict(desc_renta=0.15)),
]

SENS = [
    ("Alquiler −10%", dict(f_renta=0.90)),
    ("Alquiler −20% (ubicación periférica)", dict(f_renta=0.80)),
    ("Alquiler −20% con 60 años", dict(f_renta=0.80, T1=60)),
    ("Costo de obra +10%", dict(f_costo=1.10)),
    ("Valor de relicitación −25%", dict(f_relic=0.75)),
    ("Primer periodo de 40 años", dict(T1=40)),
    ("Primer periodo de 50 años", dict(T1=50)),
    ("Capital 7.0%", dict(r_inv=0.07)),
    ("Capital 8.0%", dict(r_inv=0.08)),
    ("Estado financia a 7.0%", dict(r_est=0.07)),
]


def plazo_minimo(r_inv, **kw):
    """Menor T1 (años) con el que los inversionistas logran r_inv y el Estado recupera el terreno a r_est."""
    for T1 in range(20, 100):  # el Código Civil limita la superficie a 99 años
        o, _ = proyecto(var(r_inv=r_inv, T1=T1, **kw))
        if o["inv_ok"] and o["vpn_est_rest"] >= 0:
            return T1
    return None


# Bono visible a la familia (diseño de la Ley 30952: S/ 500 al mes por 5 años, 70% alquiler y 30% ahorro)
BONO = dict(monto=500.0, pct_alquiler=0.70, anios=5, area_unidad=40.0, pct_ingreso=0.30)


def asequibilidad(ingresos=(2500, 3000, 3500, 4000, 4500), s=SP, p=B):
    renta_mes = renta_base(p) * s["f_renta"] / 12 * BONO["area_unidad"]  # alquiler de mercado, t0
    bono_alq = BONO["monto"] * BONO["pct_alquiler"]
    out = []
    for y in ingresos:
        paga = y * BONO["pct_ingreso"]
        brecha = renta_mes - paga
        out.append(dict(ingreso=y, renta_mercado=renta_mes, paga_30=paga, brecha=brecha,
                        cubre_bono=brecha <= bono_alq, brecha_tras_bono=brecha - bono_alq))
    ahorro = BONO["monto"] * (1 - BONO["pct_alquiler"]) * 12 * BONO["anios"]
    costo_fiscal = BONO["monto"] * 12 * BONO["anios"]
    return dict(renta_mes=renta_mes, bono_alq=bono_alq, ahorro_5a=ahorro, costo_fiscal_5a=costo_fiscal, tabla=out)


def main():
    base, fil = proyecto(SP)
    esc = []
    for k, nm, kw in ESCENARIOS:
        o, _ = proyecto(var(**kw))
        esc.append(dict(id=k, nombre=nm, **{x: o[x] for x in
                   ("tir_proy", "tir_inv", "inv_ok", "tir_est", "vpn_est_rest", "vpn_est_9", "rec", "fee", "tir_dev")}))
    sens = []
    for nm, kw in SENS:
        o, _ = proyecto(var(**kw))
        sens.append(dict(nombre=nm, **{x: o[x] for x in
                    ("tir_inv", "inv_ok", "tir_est", "vpn_est_rest", "rec")}))
    plazos = [dict(r_inv=r, T1_min=plazo_minimo(r), T1_min_alq80=plazo_minimo(r, f_renta=0.8))
              for r in (0.07, 0.075, 0.08, 0.085, 0.09)]
    res = dict(supuestos=dict(SP=SP, costos=costos_base(), renta_base=renta_base(), L=base["L"], BONO=BONO),
               base=base, escenarios=esc, sensibilidad=sens, plazos=plazos, asequibilidad=asequibilidad(),
               flujos=[{k: d[k] for k in ("t", "obra", "ocup", "renta", "opex", "reserva", "noi", "renov",
                                          "igv_neto", "cf", "f_inv", "f_est")} for d in fil[:SP["T1"] + 1]])
    with open(os.path.join(AQUI, "resultados_suelo_publico.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, default=str)
    print("Costos t0:", {k: round(v, 1) for k, v in costos_base().items()}, "renta t0:", round(renta_base(), 1),
          "terreno:", round(base["L"], 1))
    print(f"BASE E4 (propuesta): TIR proy {base['tir_proy']:.2%} inv {base['tir_inv']:.2%} ok={base['inv_ok']} "
          f"Estado {base['tir_est']:.2%} VPN@6.3% {base['vpn_est_rest']:.0f} VPN@9% {base['vpn_est_9']:.0f} "
          f"recupera {base['rec']} fee {base['fee']:.0f} dev {base['tir_dev']:.1%} precio LP {base['precio_lp']:.0f}")
    for e in esc:
        print(f"{e['id']} {e['nombre'][:58]:58s} proy {e['tir_proy']:6.2%} inv {e['tir_inv']:6.2%} ok={str(e['inv_ok']):5s} "
              f"Estado {e['tir_est']:6.2%} VPN63 {e['vpn_est_rest']:6.0f} VPN9 {e['vpn_est_9']:6.0f} rec {e['rec']} dev {e['tir_dev']:.1%}")
    for e in sens:
        print(f"  {e['nombre']:40s} inv {e['tir_inv']:6.2%} ok={str(e['inv_ok']):5s} Estado {e['tir_est']:6.2%} VPN63 {e['vpn_est_rest']:6.0f} rec {e['rec']}")
    for pz in plazos:
        print("  plazo mínimo", pz)
    a = asequibilidad()
    print("Asequibilidad:", round(a["renta_mes"]), "bono alq", a["bono_alq"], "ahorro", a["ahorro_5a"])
    for r in a["tabla"]:
        print("  ", {k: (round(v) if isinstance(v, float) else v) for k, v in r.items()})


if __name__ == "__main__":
    main()
