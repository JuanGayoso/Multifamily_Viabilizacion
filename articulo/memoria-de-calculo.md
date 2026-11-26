# Memoria de cálculo

**Vivienda para venta (BTS) frente a vivienda para renta (BTR) en Lima Moderna**

Versión 2.0 · 25 de noviembre de 2026 · Acompaña al artículo [Vivienda en renta en Lima: qué tiene que ser cierto para que compita por el suelo](financiamiento-vivienda-en-renta-peru.md)

Esta memoria describe todos los cálculos para que un tercero pueda revisarlos, reproducirlos o cambiarlos. Hay tres implementaciones equivalentes:

| Archivo | Qué es |
|---|---|
| [`modelo/modelo_multifamily.py`](../modelo/modelo_multifamily.py) | Modelo de referencia en Python. Genera `modelo/resultados.json` y todas las tablas del artículo |
| [`modelo/memoria-de-calculo.xlsx`](../modelo/memoria-de-calculo.xlsx) | Réplica con fórmulas vivas (1,634 fórmulas, 0 errores). La hoja Resumen compara Excel con Python |
| [`modelo/construir_excel.py`](../modelo/construir_excel.py) | Script que genera el Excel a partir del modelo |

**Reproducir:** `pip install numpy-financial openpyxl` → `python3 modelo/modelo_multifamily.py` → `python3 modelo/construir_excel.py` → abrir el `.xlsx` en Excel o LibreOffice (recalcula al abrir).

**Control de consistencia.** Excel y Python se compararon en el caso base y en siete variantes: régimen B, régimen C, D.Leg. 973, nota puente, sin mini-perm, cap de 6% y prima de 10%. Las TIR coinciden hasta el cuarto decimal.

---

## 1. Convenciones

- **Moneda:** soles nominales (S/). Los datos en US$ se convierten a S/ 3.41 por US$.
- **Periodo:** trimestre. *t* = 0 es la compra del terreno. Las tasas anuales se convierten a trimestrales con *r*<sub>q</sub> = (1 + *r*)<sup>1/4</sup> − 1, y las TIR trimestrales se anualizan con (1 + TIR<sub>q</sub>)<sup>4</sup> − 1.
- **Escala:** proyecto de *A* = 5,500 m² vendibles o arrendables. Los resultados se presentan por m² dividiendo entre *A*.
- **Escalamiento:** un valor base *X*<sub>0</sub> en el trimestre *t* vale *X*<sub>0</sub> · (1 + *g*)<sup>t/4</sup>.
- **Impuestos:** el IGV se modela como flujo de caja. El análisis principal es antes de Impuesto a la Renta; la sección 9 presenta la prueba después de IR.
- **Signos:** las salidas son negativas en los flujos.

## 2. Supuestos y su sustento

### 2.1 Mercado

| Parámetro | Valor | Sustento |
|---|---|---|
| Precio de oferta | US$ 1,868 por m² (con IGV) | BCRP, Nota de Estudios 16-2026, IV-2025, sector de ingresos medios. Promedio simple de los 6 distritos: (2,086 + 1,970 + 1,880 + 1,717 + 1,697 + 1,849) / 6 = 1,866.5, coincidente con el agregado del BCRP de 1,868 |
| Alquiler de oferta | US$ 119.3 por m² al año | Ídem: (125 + 132 + 116 + 115 + 100 + 128) / 6 = 119.3 |
| PER implícito | 1,868 / 119.3 = 15.7 | BCRP: 16.3 en los 12 distritos y 16.1 al II-2026 |
| Descuento oferta → cierre | 4% en ambos | Estimación. Al aplicarse igual a precio y renta, no altera la comparación relativa |
| Crecimiento de precio y renta | 2.5% anual | Inflación de largo plazo, sin crecimiento real. Meta BCRP 2% ± 1; BBVA Research proyecta 2.2% a dic-2027 |
| Crecimiento del costo de construcción y del opex | 3.0% anual | Estimación, ligeramente sobre la inflación |
| Tipo de cambio | S/ 3.41 por US$ | Nov-2026 |

Precio de cierre: *P*<sub>0</sub> = 1,868 × 3.41 × 0.96 = **S/ 6,115 por m²** con IGV.
Renta de cierre: *R*<sub>0</sub> = 119.3 × 3.41 × 0.96 × (1 + prima) = **S/ 390.5 por m² al año** (prima base de 0%).

### 2.2 Costos de desarrollo (sin IGV)

| Partida | Fórmula | Base |
|---|---|---|
| Costo directo (CD) | S/ 2,050 por m² techado × 1.30 techado/vendible | S/ 2,665 por m² vendible; CD total = S/ 14.66 millones |
| Indirectos | 12% del CD; 30% durante t1-t3 y 70% durante la obra (t4-t10) | 80% afecto a IGV |
| Contingencia | 5% del CD, durante la obra | Afecta a IGV |
| Gastos de venta BTS | 4% de la venta neta de IGV, en el trimestre de la venta | Afectos a IGV |
| Amoblado y amenities BTR | S/ 150 por m², en t9-t10 | Afectos a IGV |
| Comercialización inicial BTR | S/ 20 por m², en t10-t12 | Afecta a IGV |
| Alcabala | 3% del precio del terreno | Se paga con el terreno en *t* = 0 |

El costo de cada trimestre se escala con (1.03)<sup>t/4</sup>.

### 2.3 Opex del propietario BTR (S/ por m² al año, sin IGV, valores de *t* = 0)

| Partida | S/ por m² | Base de estimación |
|---|---|---|
| Administración del edificio | 16 | ≈5% del ingreso efectivo |
| Predial y arbitrios | 22 | Edificio completo en el tramo de 1.0% del predial sobre un autoavalúo de ≈50% del valor de mercado, más arbitrios |
| Seguros | 8 | ≈0.15% del valor |
| Rotación (corretaje, limpieza, pintura) | 7 | 25% de rotación anual × 1 mes de renta |
| Reparaciones dentro de las unidades | 8 | Estimación |
| Áreas comunes no recuperables y amenities | 6 | Estimación (el inquilino paga el mantenimiento del edificio, como en el mercado) |
| Administración, legal, cobranza, auditoría y fiduciario | 5 | Estimación |
| **Total** | **72** | ≈21% del ingreso neto estabilizado |

Del opex, 60% es fijo y 40% varía con la ocupación; 70% está afecto a IGV. La reserva de reposición es 2% del ingreso neto y se descuenta del NOI, según la metodología del contrato 11.

### 2.4 Financiamiento

| Parámetro | BTS | BTR |
|---|---|---|
| Crédito de obra: tasa | 10.0% TEA | 10.0% TEA |
| LTC sobre el costo de obra con IGV del trimestre | 65% | 55% (dimensionado a la toma del mini-perm) |
| Comisión de estructuración | 1% de la línea, en t4 | 1% de la línea, en t4 |
| Mini-perm | — | 9.0% TEA; amortización a 20 años con cuota trimestral constante; refinanciamiento en t14; LTV ≤ 60%; DSCR ≥ 1.25x; debt yield ≥ 9.5%; comisión de 1% |
| Nota puente (variante) | 45% del terreno al 12% TEA, capitalizable, cancelada en t4 | Ídem |

Sustento de las tasas: soberano SB12AGO34 6.35% (MEF, 30-set-2026). La tasa activa de medianas y grandes empresas a más de 360 días no pudo descargarse de BCRPData; las tasas son supuestos con sensibilidad (ver "Datos a verificar" en el artículo).

## 3. Modelo BTS

Para cada trimestre *t*:

1. **Ventas contratadas.** *V*<sub>t</sub> = 1[3 ≤ *t* ≤ 14] · (*A* / 12) · *P*<sub>0</sub> · (1.025)<sup>t/4</sup> (con IGV).
2. **Cobranza.**
   - Inicial: 20% · *V*<sub>t</sub> en el trimestre de la venta.
   - Saldo: 80% · *V*<sub>k</sub> en max(*k*, 11). En *t* = 11 se cobran los saldos de todas las ventas hechas hasta *t* = 11; desde ahí, el saldo se cobra en el trimestre de la venta.
3. **Venta neta de IGV.** Cobranza / 1.09, porque el IGV de la primera venta se aplica sobre una base que excluye el terreno, presumido en 50%: 18% × 50% = 9% efectivo.
4. **Costos.** Sección 2.2; gastos de venta = 4% · *V*<sub>t</sub> / 1.09.
5. **IGV.**
   - Crédito del trimestre = 18% × (partes afectas de indirectos, CD, contingencia y gastos de venta).
   - Débito = cobranza × 0.09 / 1.09.
   - Saldo: *S*<sub>t</sub> = *S*<sub>t−1</sub> + crédito<sub>t</sub> − min(*S*<sub>t−1</sub> + crédito<sub>t</sub>, débito<sub>t</sub>).
   - IGV pagado = débito − uso.
   - El saldo final no recuperado (S/ 89 por m²) se trata como pérdida, un supuesto conservador contra el BTS.
6. **Flujo no apalancado sin terreno.** *CF*<sub>u</sub> = cobranza − costos − gastos de venta − IGV de compras − IGV pagado.
7. **Crédito promotor con barrido de caja.**
   - Interés capitalizado: *I*<sub>t</sub> = *B*<sub>t−1</sub> · *r*<sub>q</sub>.
   - Si *CF*<sub>u</sub> − comisión < 0, desembolso *D*<sub>t</sub> = min(65% × costo de obra con IGV<sub>t</sub>, déficit).
   - Si es ≥ 0, repago *R*<sub>t</sub> = min(*B*<sub>t−1</sub> + *I*<sub>t</sub>, excedente).
   - *B*<sub>t</sub> = *B*<sub>t−1</sub> + *I*<sub>t</sub> + *D*<sub>t</sub> − *R*<sub>t</sub>.
8. **Flujo del capital sin terreno.** *E*<sub>t</sub> = *CF*<sub>u</sub> − comisión + *D*<sub>t</sub> − *R*<sub>t</sub>; en el último periodo se resta cualquier saldo remanente.
9. **Terreno residual.** El terreno se paga con capital en *t* = 0 y la deuda no depende de su precio. Por eso el residual es lineal:

   *L*\* = [Σ<sub>t</sub> *E*<sub>t</sub> / (1 + *r*<sub>q</sub>)<sup>t</sup>] / (1 + alcabala), con *r* = 20%.

   **Resultado: *L*\* = S/ 5.58 millones = S/ 1,015 por m² vendible.** Este es el precio de mercado del terreno en el resto del análisis. Con ese precio, la TIR del capital BTS es exactamente 20.0% (control).

Indicadores de calibración: incidencia del terreno = *L*\* / cobranza total = 15.7%; margen sobre costo = 27.7% (21.7% sobre ventas).

## 4. Modelo BTR

1. **Ocupación.** 0 hasta t10; 25%, 50%, 75% y 90% en t11-t14; 95% desde t15.
2. **Renta cobrada al inquilino** (a precio de mercado): *A* · *R*<sub>0</sub> / 4 · (1.025)<sup>t/4</sup> · ocupación<sub>t</sub> · (1 − 1% de incobrables).
3. **Ingreso neto del propietario, según el régimen de IGV:**
   - A (vigente): renta / 1.18. El débito, 18% del ingreso neto, se compensa con el crédito.
   - B (exonerado): renta completa. El IGV de obra y de opex es costo.
   - C (hipotético): renta completa. El IGV de obra y de opex se devuelve con 2 trimestres de rezago.
4. **Opex.** *A* · 72 / 4 · (1.03)<sup>t/4</sup> · [0.6 + 0.4 · ocupación / 0.95], desde t11.
5. **NOI** = ingreso neto − opex − reserva (2% del ingreso neto) − [IGV de opex, solo en el régimen B].
6. **Crédito fiscal (régimen A).**
   - Adición = IGV de obra + IGV de opex. Con el D.Leg. 973 activo, el IGV de obra hasta t10 se devuelve con 2 trimestres de rezago y no se suma al saldo.
   - Uso = min(saldo + adición, débito).
   - En el caso base el saldo llega a S/ 3.35 millones al terminar la obra, baja unos S/ 72 mil por trimestre y queda en S/ 2.62 millones en t22.
7. **Salida en t22.**
   - Valor = NOI de t23-t26 / cap (6.5%).
   - Ingreso neto = valor × (1 − 1.5%) + saldo de crédito × (1 − 25%) en el régimen A, porque el crédito se transfiere con el vehículo y el comprador lo valoriza con descuento.
   - **Variante "venta por unidades":** ingreso = *A* · *P*<sub>0</sub> · (1.025)<sup>22/4</sup> · (1 − 7% por unidad usada) · 0.92 (valor presente de vender en ≈8 trimestres) / 1.09 · (1 − 4%), más el crédito fiscal usado contra el IGV de esas ventas.
8. **Flujo no apalancado sin terreno** = renta cobrada − opex − reserva − IGV de opex − costos − IGV de obra − IGV pagado + devoluciones, más la salida en t22.
9. **Crédito de obra.** Misma mecánica que en el BTS, con LTC de 55% y base = costo + IGV hasta t12. Se cancela en t14 con su saldo más intereses.
10. **Mini-perm en t14.**
    - NOI prospectivo = Σ NOI de t15-t18 = S/ 1.410 millones. Valor = NOI / 6.5% = S/ 21.70 millones.
    - Cuota por sol prestado: *c* = *r*<sub>q</sub> / [1 − (1 + *r*<sub>q</sub>)<sup>−80</sup>]; constante anual *k* = 4*c* = 10.60%.
    - Límites:
      - LTV: 60% × 21.70 = S/ 13.02 millones.
      - DSCR: 1.410 / (1.25 × 0.1060) = **S/ 10.64 millones**.
      - Debt yield: 1.410 / 9.5% = S/ 14.85 millones.
    - Monto = mínimo = S/ 10.64 millones (S/ 1,935 por m²), con LTV de 49%. Lo limita el DSCR.
    - Saldo del crédito de obra en t14: S/ 2,554 por m². **Hueco de refinanciamiento: S/ 619 por m², que aporta el capital.**
    - Servicio trimestral desde t15. El saldo en t22 (96% del monto) se cancela con la venta.
11. **Flujo del capital** = no apalancado − comisión + desembolsos − repagos + mini-perm neto de comisión − servicio − cancelación.
12. **Terreno residual.**
    - Vara estricta: VAN del flujo del capital al 14%, dividido entre 1.03.
    - Vara laxa: VAN del flujo no apalancado a *r*<sub>u</sub> = cap + *g*, dividido entre 1.03.
    - Ratio = residual BTR / residual BTS.
13. **YoC** = NOI de t15-t18 / (costo de desarrollo sin terreno + [IGV de obra en el régimen B] + terreno × 1.03).

### 4.1 Cascada del NOI estabilizado (S/ por m² al año, Σ t15-t18)

| | S/ por m² |
|---|---|
| Renta potencial: 406.7 / (0.95 × 0.99) | 432.4 |
| Renta cobrada | 406.7 |
| Ingreso neto de IGV (/1.18) | 344.7 |
| Opex | −81.3 |
| Reserva | −6.9 |
| NOI | 256.4 |

YoC = 256.4 / (3,462.9 + 1,014.6 × 1.03) = 256.4 / 4,508 = **5.69%**.

## 5. Benchmark: arrendador persona natural (hoja "Individual")

Por m²:

| Concepto | Valor |
|---|---|
| Precio | S/ 6,115 con IGV |
| Costos de compra | 1.5% |
| Renta | S/ 390.5 |
| Vacancia | 8% |
| Corretaje | 0.5 meses al año |
| Predial | 0.2% del precio |
| Mantenimiento en vacancia | 12% de la renta mensual × vacancia |
| IR | 5% de la renta cobrada |

- Ingreso neto = 390.5 × 0.92 − 390.5 × 0.5/12 − 0.002 × 6,115 − 0.08 × 0.12 × 390.5 − 0.05 × 390.5 × 0.92 = **S/ 309.1**.
- Rendimiento neto = 309.6 / (6,115 × 1.015) = **4.98%**.
- TIR a 10 años: compra en el año 0; ingreso neto creciendo 2.5% anual; venta en el año 10 a *P*<sub>0</sub> · 1.025<sup>10</sup> · 0.97. **Resultado: 7.1%.**

## 6. Resultados del caso base

| Indicador | Valor |
|---|---|
| Terreno residual BTS (20%) | S/ 1,015 por m² |
| TIR del capital BTS / no apalancada | 20.0% / 17.2% |
| NOI BTR estabilizado | S/ 256 por m² al año |
| YoC / cap / margen de desarrollo | 5.69% / 6.50% / −81 pb |
| TIR no apalancada BTR / del capital (terreno a mercado) | 0.5% / −5.4% |
| Terreno residual BTR: vara laxa / estricta | −S/ 195 / −S/ 452 por m² |
| Mini-perm: monto / LTV / DSCR mínimo / balloon | S/ 1,935 por m² / 49% / 1.24x / 96% |

El DSCR mínimo de 1.24x, apenas bajo el 1.25x de dimensionamiento, se da en t15: el préstamo se dimensiona con el NOI de los cuatro trimestres siguientes y el primero es el más bajo.

## 7. Escenarios

Los valores están en `modelo/resultados.json` y en la hoja "Escenarios". El terreno es el de mercado del caso base, salvo en los cambios que también afectan al BTS (costo de obra, tasa de obra), donde se recalcula.

| Escenario | YoC | TIR no apalancada | TIR del capital |
|---|---|---|---|
| Base (régimen A) | 5.69% | 0.5% | −5.4% |
| A + D.Leg. 973 | 5.69% | 1.2% | −5.0% |
| Régimen B | 6.00% | 2.6% | −2.4% |
| Régimen C (hipotético) | 7.04% | 6.6% | 4.2% |
| Nota puente | 5.69% | 0.5% | −6.0% |
| Sin mini-perm | 5.69% | 0.5% | −2.0% |
| Mini-perm solo intereses | 5.69% | 0.5% | −6.7% |
| Financiamiento verde | 5.67% | 0.4% | −5.4% |
| Construcción industrializada (−5% de CD) | 5.73% | 0.7% | −4.9% |
| Prima de renta +5% | 6.06% | 2.0% | −3.0% |
| Cap 6.00% / 7.00% | 5.69% | 2.1% / −1.0% | −2.6% / −8.1% |
| Vacancia de 8% | 5.45% | −0.5% | −6.9% |
| Opex +20% | 5.33% | −1.0% | −7.9% |
| A / B con venta por unidades | 5.69% / 6.00% | 6.4% / 4.4% | 4.4% / 0.8% |
| A / B con tenencia de 10 años | 5.69% / 6.00% | 5.1% / 6.2% | 2.9% / 4.4% |
| B + cap 6.0% + prima 5% | 6.39% | 6.1% | 3.5% |
| Toda la ingeniería financiera (A) | 5.70% | 1.2% | −5.0% |
| B + toda la ingeniería + cap 6.0% + prima 5% | 6.43% | 6.2% | 3.9% |
| Nicho: B + prima 10% + cap 6.0% + terreno al 50% | 7.55% | 11.1% | 11.8% |
| Nicho: B + prima 20% + cap 6.0% + terreno a mercado | 7.55% | 10.7% | 11.0% |
| Nicho: B + prima 10% + cap 6.0% + terreno aportado | 8.51% | 15.6% | 21.2% |

**Sensibilidad al precio del terreno** (régimen A):

| Terreno | TIR no apalancada | TIR del capital | YoC |
|---|---|---|---|
| 0% del mercado | 7.2% | 4.4% | 7.41% |
| 25% | 5.2% | 1.1% | 6.89% |
| 50% | 3.4% | −1.4% | 6.43% |
| 75% | 1.9% | −3.6% | 6.04% |
| 100% | 0.5% | −5.4% | 5.69% |

**Sensibilidad del terreno de mercado (BTS):**

| Caso | S/ por m² | Incidencia |
|---|---|---|
| Base | 1,015 | 15.7% |
| Precio −5% | 833 | 13.6% |
| Ventas en 16 trimestres | 847 | 13.0% |
| TIR exigida de 18% / 22% | 1,081 / 953 | 16.8% / 14.8% |
| CD +10% | 752 | 11.7% |

## 8. Mapa de viabilidad

Ratio entre el terreno residual BTR con la vara laxa (*r* = cap + 2.5%) y el terreno de mercado (ver la tabla 9 del artículo y la hoja "Mapa"). El ratio llega a 1.00 o más solo en estos casos:

- **Régimen B:** prima de 10% con cap de 5.5%; prima de 20% con cap ≤ 6.0%; prima de 30% con cap ≤ 7.0%.
- **Régimen A:** prima de 20% con cap de 5.5%; prima de 30% con cap ≤ 6.0%.

Con la vara estricta (capital al 14%), el umbral es más exigente: solo régimen B con prima de 20% y cap de 5.5% (ratio 1.03), y prima de 30% con cap ≤ 6.0%.

## 9. Prueba después de Impuesto a la Renta

Supuestos:

- Tasa de 29.5%.
- BTS: reconoce la utilidad al cobrar el saldo, en proporción a la venta neta reconocida.
- BTR: deprecia 5% anual el costo de desarrollo desde t11; la reserva no es deducible al devengarse; ganancia de capital en la venta = ingreso neto − costo no depreciado − terreno.
- Pérdidas arrastrables sin límite (simplificación favorable al BTR).

| Caso | TIR no apalancada BTS | TIR no apalancada BTR |
|---|---|---|
| Régimen A, venta en bloque | 12.3% | −0.4% |
| Régimen B, venta en bloque | 12.3% | 1.8% |
| Régimen A, venta por unidades | 12.3% | 4.0% |

## 10. Limitaciones conocidas del modelo

1. Precios y rentas de oferta (BCRP/Urbania) y no de cierre.
2. Costo directo de fuentes débiles; validado solo de forma indirecta por la incidencia del terreno BTS.
3. Régimen B con venta por unidades: no se modela la prorrata del crédito fiscal, lo que perjudica algo a ese caso.
4. La hoja Excel admite un trimestre de salida de hasta 22; para tenencias largas, usar Python (`q_salida`).
5. No se modelan coberturas de tasa, riesgo cambiario (todo en soles) ni costos de estructuración de la FIBRA.
6. El IR de primera categoría de la persona natural se aplica sobre la renta cobrada. No se modela la informalidad de parte del mercado de alquiler, que ampliaría la brecha contra el multifamily.

## 11. Mapa del Excel

| Hoja | Filas clave |
|---|---|
| Supuestos | Todos los insumos (azul) y los derivados *P*<sub>0</sub>, *R*<sub>0</sub>, tasas trimestrales y *r*<sub>u</sub> |
| BTS | 7-10 ventas y cobranza · 12-16 costos · 17-20 IGV · 21 flujo no apalancado · 22-28 crédito promotor · 29-31 flujos del capital |
| BTR | 7-15 operación y NOI · 16-23 costos · 24-28 IGV y devoluciones · 29-30 flujo no apalancado · 31-36 crédito de obra · 37-41 mini-perm · 42-44 flujos del capital · 49-52 salida · 55-64 dimensionamiento del mini-perm |
| Resumen | Resultados de Excel junto a los de Python, con columna de diferencias |
| Individual | Benchmark de la persona natural con fórmulas |
| Escenarios, Mapa, Distritos, DespuesIR | Tablas de valores del script (no se recalculan) |
