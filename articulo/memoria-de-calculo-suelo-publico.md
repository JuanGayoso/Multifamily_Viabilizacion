# Memoria de cálculo: vivienda en renta sobre suelo público (artículo 2)

Versión 1.0 · 26 de noviembre de 2026

Acompaña al artículo [`btr-y-brecha-de-vivienda-lima-callao.md`](btr-y-brecha-de-vivienda-lima-callao.md). Sirve para que un tercero pueda reproducir cada número del artículo.

- Script: [`modelo/modelo_suelo_publico.py`](../modelo/modelo_suelo_publico.py)
- Resultados: [`modelo/resultados_suelo_publico.json`](../modelo/resultados_suelo_publico.json)
- Hoja con fórmulas vivas: [`modelo/memoria-suelo-publico.xlsx`](../modelo/memoria-suelo-publico.xlsx), generada por `modelo/construir_excel_suelo_publico.py`

La hoja replica el caso base con 2,054 fórmulas. Su hoja "Resumen" compara cada indicador con el script: la diferencia es cero en los doce indicadores, salvo errores de redondeo del orden de 10⁻¹⁵.

---

## 1. Pregunta que se calcula

¿Puede un edificio de vivienda en renta (BTR) construido sobre un terreno del Estado, cedido en derecho de superficie, cumplir dos condiciones a la vez?

1. Pagar a sus inversionistas el retorno que exigen.
2. Devolverle al Estado el valor de mercado del terreno con un retorno al menos igual a su costo de financiamiento.

Si se cumplen ambas, **el Estado no subsidia el modelo de negocio**: presta un activo y lo cobra. Si no se cumplen, la diferencia es un subsidio y debe reconocerse como tal.

## 2. Mecánica del modelo

Flujos anuales en soles nominales, por m² vendible. Para un edificio de 5,500 m² (unos 137 departamentos de 40 m²) hay que multiplicar por 5,500. El análisis es antes de Impuesto a la Renta.

| Paso | Qué ocurre | Fórmula o regla |
|---|---|---|
| 0 | El Estado aporta el terreno en t = 0 | Valor = L = residual BTS del artículo 1 = S/ 1,014.6 por m² vendible |
| 1-3 | Obra en tres años (15% / 50% / 35%) | Obra_t = −capex × s_t × (1 + g_c)^t |
| 3-5 | Colocación: ocupación 0%, 60% y luego 95% | — |
| ≥ 4 | Operación | Renta_t = renta₀ × (1 + g_r)^t × ocup_t × (1 − incobrables) |
| | | Opex_t = opex × (1 + g_o)^t × [fijo + (1 − fijo) × ocup_t / 95%] × (1 + 70% × 18%) |
| | | NOI_t = Renta_t − Opex_t − 2% × Renta_t |
| 20 y 35 | Renovaciones mayores de 10% del costo, escaladas | Se omite la que cae en los últimos dos años de T1; la asume el nuevo operador |
| 1…T1 | Cascada del flujo del proyecto CF_t = Obra + NOI + Renovación | (a) inversionistas hasta su saldo con r_inv; (b) Estado hasta su saldo con r_est; (c) excedente: 50% al Estado y 50% a inversionistas |
| T1 | Reversión sin pago y relicitación | El Estado cobra Fee = Σ_{t=T1+1}^{T1+T2} NOI_t / (1 + r_inv)^(t−T1) − 15% × costo × (1 + g_c)^T1 |

**Saldos de la cascada.**

- Inversionistas: B_inv,t = B_inv,t−1 × (1 + r_inv) + aportes − pagos.
- Estado: B_est,t = B_est,t−1 × (1 + r_est) − pagos, con B_est,0 = L.
- Cuando CF_t < 0 (obra o renovación), lo aportan los inversionistas y se suma a su saldo.

**Régimen tributario.** El caso base usa el régimen B: alquiler de vivienda exonerado del IGV, con el IGV de obra y de opex como costo. Es la paridad con el arrendador persona natural y el estándar de Colombia y Chile (artículo 2, §4). El escenario E0 usa el régimen A, el vigente: renta ÷ 1.18 y crédito fiscal recuperado contra el débito.

**Etapa de desarrollo.** Se supone que en el año 5 el desarrollador vende el derecho de superficie estabilizado a un inversionista de largo plazo (FIBRA, AFP, aseguradora).

- Precio = VP a r_lp de los flujos de los inversionistas de los años 6 a T1.
- TIR de desarrollo = TIR de [flujos de los años 0-5 + precio en el año 5].

## 3. Supuestos

H = hecho con fuente; E = estimación; O = opinión profesional.

| Supuesto | Valor | Tipo | Sustento |
|---|---|---|---|
| Alquiler de oferta (Lima Moderna) | US$ 119.3 por m² al año | H | BCRP, Nota de Estudios 16-2026 (IV trim. 2025) |
| Tipo de cambio | S/ 3.41 | H | BCRP, nov-2026 |
| Descuento oferta → cierre | 4% | E | Igual que el artículo 1 |
| Renta de cierre t0 (renta₀) | S/ 390.5 por m² alquilado al año | H+E | 119.3 × 3.41 × 0.96 |
| Ocupación estabilizada / incobrables | 95% / 1% | E | Artículo 1 |
| Opex sin IGV | S/ 72 por m² al año; 60% fijo; 70% gravado | E | Artículo 1, memoria §4 |
| Reserva de reposición | 2% de la renta | E | Artículo 1 |
| Crecimiento: renta / costo / opex | 2.5% / 3.0% / 3.0% | E | Artículo 1 |
| Costo sin terreno (sin IGV) | S/ 3,288.1 por m² | E | Directo 2,665 + indirectos 12% + contingencia 5% + FF&E 150 + comercialización 20 |
| IGV de obra (costo en régimen B) | S/ 580.3 por m² | E | 18% sobre la parte gravada |
| Capex régimen B | S/ 3,868.4 por m² | E | 3,288.1 + 580.3 |
| Valor del terreno (L) | S/ 1,014.6 por m² vendible | E | Residual BTS al 20% (artículo 1, tabla 3) |
| **r_inv**: costo combinado del capital por etapas | **7.5%** nominal en soles | **O, supuesto clave** | Ver nota abajo |
| r_est: costo de financiamiento del Estado | 6.3% | H | Bono soberano en soles a ~8-10 años: SB12AGO34 6.35% (MEF, 30-set-2026) |
| T1 / T2 | 45 / 30 años | O | Mínimo con holgura (§5.3) |
| Reparto del excedente al Estado | 50% | O | Variable a competir en la licitación |
| r_lp: retorno del comprador en el año 5 | 7.0% | E | Activo estabilizado y sin riesgo de obra |

**Por qué 7.5% es el supuesto que más hay que vigilar.** Es un promedio ponderado en el tiempo, no la tasa de un solo inversionista:

- **Obra (años 0-3):** capital de desarrollo de 12%-14% y crédito de obra de 10%. Ver artículo 1, tabla 2.
- **Operación (años 4 a T1):** deuda de largo plazo en soles a 7%-7.5%. Equivale a bonos de titulización o a crédito de AFP y aseguradoras con spread sobre un soberano de 6.3%-7.0%.
- **Capital de largo plazo:** FIBRA o fondos con rendimiento real de 4%-4.5%, es decir, 6.5%-7% nominal.

Como la obra pesa poco frente a 40 años de operación, el promedio converge a la tasa de largo plazo. Es una estimación: no hay transacciones residenciales de largo plazo en el Perú que la validen. La sensibilidad de la §5.2 muestra qué pasa con 7% y con 8%.

## 4. Resultado base (E4: régimen B, r_inv 7.5%, T1 = 45)

| Indicador | Valor | Lectura |
|---|---|---|
| NOI estabilizado (año 6) | S/ 320.6 por m² | Renta 426.0 − opex 96.8 − reserva 8.5 |
| Yield on cost sin terreno (año 6) | 8.29% | 320.6 / 3,868.4. Con terreno a mercado sería ~6.6% |
| TIR del proyecto (sin terreno) | 8.15% | Flujo hasta T1 |
| TIR de los inversionistas | 7.50% | Cobran su retorno completo; saldo en cero en el año 37 |
| Flujos al Estado antes de T1 | S/ 5,666 por m² (nominal) | Años 37-45, por la cascada |
| Valor de relicitación cobrado en T1 | S/ 10,109 por m² (nominal, año 45) | VP a 7.5% del NOI de los años 46-75, menos la renovación de 15% |
| TIR del Estado sobre su terreno | 6.66% | Mayor que su costo de 6.3% |
| VPN del Estado a 6.3% | **+S/ 160 por m²** (≈ S/ 0.9 millones por edificio) | Positivo: no hay subsidio en valor presente |
| VPN del Estado a 9% | −S/ 615 por m² | A la vara de un inversionista privado, el Estado cede valor (§6) |
| Año de recuperación del terreno | 45 | La recuperación es tardía (§6) |
| TIR de la etapa de desarrollo | 9.4% (11.5% si r_lp = 6.5%; 7.5% si r_lp = 7.5%) | Baja para un desarrollador a riesgo: §6 |

**Comprobación aritmética del NOI del año 6.**

- Factor de crecimiento de la renta: 1.025⁶ = 1.1597.
- Renta: 390.5 × 1.1597 × 0.95 × 0.99 = **426.0**.
- Factor de crecimiento del opex: 1.03⁶ = 1.1941.
- Opex: 72 × 1.1941 × (0.6 + 0.4 × 0.95/0.95) × (1 + 0.7 × 0.18) = 85.98 × 1.126 = **96.8**.
- Reserva: 2% × 426.0 = **8.5**.
- NOI: 426.0 − 96.8 − 8.5 = **320.6**.

## 5. Escenarios, sensibilidad y plazo mínimo

### 5.1 Escenarios

| Id | Escenario | TIR inversionistas | ¿Cumple r_inv? | TIR Estado | VPN Estado @6.3% | Recupera |
|---|---|---|---|---|---|---|
| E0 | IGV actual, capital 9%, 30 años | 6.12% | No | 5.35% | −239 | No |
| E1 | Paridad IGV, capital 9%, 45 años | 8.15% | No | 4.80% | −480 | No |
| E2 | Paridad IGV, capital 8%, 45 años | 8.00% | Sí | 5.58% | −266 | No |
| E3 | Paridad IGV, capital 7.5%, 40 años | 7.50% | Sí | 6.38% | +30 | Año 40 (en el límite) |
| **E4** | **Propuesta: paridad IGV, capital 7.5%, 45 años** | **7.50%** | **Sí** | **6.66%** | **+160** | **Año 45** |
| E5 | Paridad IGV, capital 7.5%, 50 años | 7.50% | Sí | 6.85% | +268 | Año 50 |
| E6 | E4 con descuento de 15% al inquilino financiado con el terreno | 6.52% | No | 4.56% | −531 | No |

### 5.2 Sensibilidad sobre E4

| Variación | TIR inversionistas | ¿Cumple? | TIR Estado | VPN Estado @6.3% |
|---|---|---|---|---|
| Alquiler −10% | 7.08% | No | 4.81% | −477 |
| Alquiler −20% (ubicación periférica) | 5.92% | No | 4.28% | −586 |
| Alquiler −20% con 60 años | 6.58% | No | 3.69% | −786 |
| Costo de obra +10% | 7.43% | No | 5.20% | −380 |
| Valor de relicitación −25% | 7.50% | Sí | 6.30% | −1 |
| Primer periodo de 40 años | 7.50% | Sí | 6.38% | +30 |
| Primer periodo de 50 años | 7.50% | Sí | 6.85% | +268 |
| Capital 7.0% | 7.00% | Sí | 7.33% | +492 |
| Capital 8.0% | 8.00% | Sí | 5.58% | −266 |
| Estado se financia al 7.0% | 7.50% | Sí | 6.66% | −129 |

### 5.3 Primer periodo mínimo

Es el T1 mínimo con el que los inversionistas cobran r_inv y el VPN del Estado a 6.3% es ≥ 0. El Código Civil, art. 1030, limita el derecho de superficie a 99 años.

| Costo del capital | T1 mínimo, Lima Moderna | T1 mínimo con alquiler −20% |
|---|---|---|
| 7.0% | 31 años | No existe (≤ 99) |
| 7.5% | 36 años | No existe |
| 8.0% | 59 años | No existe |
| 8.5% | No existe | No existe |
| 9.0% | No existe | No existe |

**Por qué 45 años y no 36.** Con 36 años el VPN del Estado es apenas positivo. Si el alquiler o el costo se desvían algo, pasa a negativo. Con 45 años el margen es de S/ 160 por m², y aun así un alquiler 10% menor lo elimina. El plazo no se elige para maximizar el cobro del Estado. Se elige para que la operación no se vuelva un subsidio con el primer error de estimación.

## 6. Lo que el modelo no resuelve (y se reporta en el artículo)

1. **El margen es estrecho.** La propuesta pasa la prueba de "sin subsidio" con un VPN de +S/ 160 por m² sobre un terreno de S/ 1,015. Alquiler −10%, costo +10% o capital al 8% la vuelven negativa. La licitación competitiva (§7 del artículo) es la herramienta para no regalar el margen, pero no lo crea.
2. **La recuperación del Estado es tardía y depende de la relicitación.** El 64% del valor nominal que recibe el Estado llega en el año 45 como pago del segundo periodo (10,109 de 15,775). Con un valor de relicitación 25% menor, el VPN queda en cero.
3. **La periferia no cierra.** Con alquileres 20% menores que en Lima Moderna, ningún plazo permitido por el Código Civil funciona. El esquema es para suelo público bien ubicado, no para cualquier terreno.
4. **La etapa de desarrollo rinde poco (9.4% sin deuda).** Un desarrollador a riesgo pediría 12%-14%. Por eso la propuesta es de *forward funding*: el inversionista de largo plazo compromete el capital desde la licitación y el desarrollador cobra un honorario más un incentivo por costo y plazo. Ver contrato 12, cláusula 5.
5. **Antes de IR.** El IR de 29.5% sobre la utilidad del operador reduce el retorno disponible. Con una FIBRA (Ley 30532) como tenedor de largo plazo, el impuesto se traslada al partícipe. Ver "Datos a verificar" sobre si una FIBRA puede tener un derecho de superficie.
6. **No modela el riesgo de que el Estado incumpla** (cambio de reglas, revisión unilateral). Ese riesgo sube r_inv; la mitigación es contractual (contrato 12, cláusulas 9 y 14).

## 7. Asequibilidad: bono visible a la familia

Cálculo en la hoja "Asequibilidad" (con fórmulas):

- Alquiler de mercado de un departamento de 40 m² en t0: 390.5 / 12 × 40 = **S/ 1,302 al mes**.
- Bono (diseño de la Ley 30952, Renta Joven): S/ 500 al mes por hasta 5 años. De eso, S/ 350 (70%) van al alquiler y S/ 150 (30%) a una cuenta de ahorro.
- Ahorro acumulado: 150 × 12 × 5 = **S/ 9,000**, para la cuota inicial de Techo Propio o del Nuevo Crédito Mivivienda.
- Costo fiscal por hogar: 500 × 12 × 5 = **S/ 30,000** en cinco años.

| Ingreso del hogar | Paga 30% | Brecha sin bono | Brecha con bono | ¿Cubre? |
|---|---|---|---|---|
| S/ 2,500 | 750 | 552 | 202 | No |
| S/ 3,000 | 900 | 402 | 52 | No (casi) |
| S/ 3,500 | 1,050 | 252 | −98 | Sí |
| S/ 4,000 | 1,200 | 102 | −248 | Sí |
| S/ 4,500 | 1,350 | −48 | −398 | Sí (sin bono) |

Ingreso mínimo atendido con el bono: (1,302 − 350) / 0.30 = **S/ 3,173 al mes**.

El tramo objetivo, de S/ 3,200 a S/ 4,500, se cruza con el tope de ingreso de Techo Propio para compra de vivienda nueva (S/ 3,715) y queda por debajo del ingreso que hoy exige un crédito hipotecario para la vivienda nueva más barata de Lima (~S/ 5,000, según Proper, may-2026). Para hogares con ingresos menores a ~S/ 2,700, el instrumento adecuado es Techo Propio en Construcción en Sitio Propio o Mejoramiento, no el alquiler en Lima Moderna.

El bono **no toca la cascada**: el inquilino paga la renta de mercado (su parte más el bono). Por eso el retorno del terreno no cambia. El escenario E6 muestra lo contrario: un descuento financiado con el terreno hace que el Estado pierda S/ 531 por m² en valor presente, un subsidio escondido.

## 8. Cómo reproducir

```bash
cd modelo
python3 modelo_suelo_publico.py             # imprime resultados y escribe resultados_suelo_publico.json
python3 construir_excel_suelo_publico.py    # genera memoria-suelo-publico.xlsx
# recalcular las fórmulas con LibreOffice (p. ej., el script recalc.py del entorno) antes de abrirla en un visor que no calcule
```

Para cambiar un supuesto en la hoja, se edita la celda azul de "Supuestos". Las hojas Escenarios, Sensibilidad y Plazos son valores del script: hay que volver a correrlo para actualizarlas.

## 9. Control de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 26-nov-2026 | Primera versión. En la revisión interna se corrigió un error: la renta se cobraba sobre el 100% del área y no sobre el 95% ocupado. Eso sobrestimaba la renta en 5.3% y el VPN del Estado en ~S/ 460 por m². Con la corrección, el plazo propuesto pasó de 40 a 45 años. |
